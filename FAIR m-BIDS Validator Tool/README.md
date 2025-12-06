[![.github/workflows/build-test-deploy.yml](https://github.com/bids-standard/python-validator/actions/workflows/build-test-deploy.yml/badge.svg)](https://github.com/bids-standard/python-validator/actions/workflows/build-test-deploy.yml)
[![codecov](https://codecov.io/gh/bids-standard/python-validator/graph/badge.svg?token=5iz5rfzv93)](https://codecov.io/gh/bids-standard/python-validator)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3688707.svg)](https://doi.org/10.5281/zenodo.3688707)
[![PyPI version](https://badge.fury.io/py/bids-validator.svg)](https://badge.fury.io/py/bids-validator)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/bids-validator)](https://anaconda.org/conda-forge/bids-validator)

# Python BIDS-Validator

This is a library of helper functions written in Python,
for use with BIDS compliant applications written in this language.

The main function determines if a file path is compliant with the BIDS specification.

## Installation

To install with pip:

```
python -m pip install bids_validator
```

To install with conda:

```
conda install bids-validator
```

## Quickstart

1. Open a Python terminal and type: `python`
1. Import the BIDS Validator package `from bids_validator import BIDSValidator`
1. Check if a file is BIDS compatible `BIDSValidator().is_bids('/relative/path/to/a/bids/file')`
1. Note, the file path must be relative to the root of the BIDS dataset, and
  a leading forward slash `/` must be added to the file path.


### Example

```Python
from bids_validator import BIDSValidator

validator = BIDSValidator()

filepaths = ["/sub-01/anat/sub-01_rec-CSD_T1w.nii.gz", "/sub-01/anat/sub-01_acq-23_rec-CSD_T1w.exe"]
for filepath in filepaths:
    print(validator.is_bids(filepath))  # will print True, and then False
```

Note, the file path must be relative to the root of the BIDS dataset, and a
leading forward slash `/` must be added to the file path.


<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
