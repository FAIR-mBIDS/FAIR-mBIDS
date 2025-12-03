import hashlib
import csv
from pathlib import Path

# ---------------- CONFIG ----------------
# Set the dataset root directory (assumes you run this script from the dataset root)
ROOT = Path('.')  

# Metadata folder to store output CSV/TSV tables
METADATA_DIR = ROOT / 'metadata'
METADATA_DIR.mkdir(exist_ok=True)  # create folder if it doesn't exist

# Dataset-level ID (constant for the dataset)
GDID = "gds_ds005795_subset1"

# Salt used for subject-level hashing (keeps subject IDs pseudonymized)
# IMPORTANT: do NOT publish this salt if you want subject anonymity
GSID_SALT = "fixed_salt_for_this_example_v1"

# ---------------- HELPER FUNCTION ----------------
def hash_short(s, length=24):
    """
    Return the first `length` characters of a SHA-256 hash of the input string.
    
    This is used to generate:
      - GUId-Key: unique data item ID
      - GSId: pseudonymized subject ID
    """
    h = hashlib.sha256(s.encode()).hexdigest()
    return h[:length]

# ---------------- FILE EXTENSIONS ----------------
# Only process files relevant to BIDS datasets
exts = {'.nii', '.nii.gz', '.edf', '.set', '.tsv', '.tsv.gz', '.json', '.bdf', '.vhdr', '.vhdr.gz'}

# ---------------- WALK THROUGH DATASET ----------------
rows = []  # list to store all file metadata and IDs

for p in sorted(ROOT.rglob('*')):  # recursively walk through all files
    if not p.is_file():
        continue  # skip directories

    # Skip metadata folder itself to avoid infinite recursion
    if p.match('metadata/*'):
        continue

    # Skip hidden/system files (starting with '.')
    if any(part.startswith('.') for part in p.parts):
        continue

    # Skip files that do not match BIDS-relevant extensions
    if not any(str(p).endswith(ext) for ext in exts):
        continue

    # Get file path relative to dataset root, e.g., 'sub-01/anat/file.nii.gz'
    rel = p.relative_to(ROOT).as_posix()

    # ---------------- SUBJECT ID ----------------
    # Try to infer subject ID from the folder name (e.g., 'sub-01')
    subject = next((part for part in p.parts if part.startswith('sub-')), 'sub-unknown')

    # ---------------- GENERATE IDS ----------------
    # GUId-Key: unique ID for this file
    guid = "guid_" + hash_short(rel, length=24)

    # GSId: pseudonymized subject ID (all files of the same subject get same GSId)
    gsid = "gs_" + hash_short(GSID_SALT + "_" + subject, length=11)

    # GDId: dataset ID (same for all files)
    gdid = GDID

    # ---------------- INFER MODALITY ----------------
    # Try to guess the data modality from file/folder name
    parent = p.parent.name
    if 'anat' in parent:
        modality = 'T1w' if 'T1w' in p.name else 'anat'
    elif 'eeg' in parent:
        modality = 'EEG'
    elif 'func' in parent:
        modality = 'fMRI'
    elif 'beh' in parent or 'behav' in parent:
        modality = 'behavioral'
    elif 'physio' in p.name or 'physio' in parent or 'mod-' in p.name:
        modality = 'Physio'
    else:
        modality = parent  # fallback: use folder name

    # ---------------- ADD TO LIST ----------------
    rows.append({
        'GUId-Key': guid,
        'GSId': gsid,
        'GDId': gdid,
        'Modality': modality,
        'FilePath': rel
    })

# ---------------- WRITE CSV ----------------
csv_path = METADATA_DIR / 'identifiers_table.csv'
with csv_path.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['GUId-Key','GSId','GDId','Modality','FilePath'])
    writer.writeheader()  # write column headers
    for r in rows:
        writer.writerow(r)  # write each row

# ---------------- WRITE TSV ----------------
tsv_path = METADATA_DIR / 'identifiers_table.tsv'
with tsv_path.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['GUId-Key','GSId','GDId','Modality','FilePath'], delimiter='\t')
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print(f"Wrote {len(rows)} entries to {csv_path} and {tsv_path}")
