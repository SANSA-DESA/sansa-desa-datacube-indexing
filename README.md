# SANDA-DESA datacube indexing

This repository contains code for generating [opendatacube]'s dataset documents from SPOT datasets that have already 
been processed to ARD. It expects ARD SPOT datasets to be in a format similar to the datasets being produced in 
scope of the DESA project.

## Installation

This project expects to be run on a linux machine that has conda installed.

1. Clone this repo

   This repo is currently set to be private. In order to be able to clone it you need either:

   - To have a github user that is part of the `SANSA-DESA` organization
   - To be on the `sansa-desa-db` machine. This repo has been configured to accept operations from that machine
     by means of using a deploy key. Check [github's documentation on deploy keys](https://docs.github.com/en/developers/overview/managing-deploy-keys#deploy-keys) 
     for more info.

1. Create the conda environment from the repo's `spec-file.txt`:

   ```
   conda create --name sansa-desa-datacube-indexing --file spec-file.txt
   ```


## Running

Activate the conda environment and run the `main.py` module:

```
conda activate sansa-desa-datacube-indexing
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