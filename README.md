# SANDA-DESA datacube indexing

This repository contains code for generating [opendatacube]'s dataset documents from SPOT datasets that have already 
been processed to ARD. It expects ARD SPOT datasets to be in a format similar to the datasets being produced in 
scope of the DESA project.

## Installation

This project expects to be run on a linux machine that has conda installed.

1. Clone this repo

1. Create the conda environment from the repo's `spec-file.txt`:

   ```
   conda create --name $(basename $(pwd)) --file spec-file.txt
   ```


## Running

Activate the conda environment and run the `main.py` module:

```
python sansa_desa_datacube_indexing/main.py --help
```

The `--help` flag shows available options. Example:

```
python sansa_desa_datacube_indexing/main.py  \
    --verbose \
    --dataset-pattern='S7-*_PSH.pix' \
    --output-path=$(pwd)/test.yml \
    spot7-ard \
    /datadisk/data/SANSA-DESA/modified-s-7-example-odc/

```

[opendatacube]: https://datacube-core.readthedocs.io/en/latest/ops/dataset_documents.html