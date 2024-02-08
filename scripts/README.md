# Scripts 

This directory contains scripts to be run. 

### `update.sh`

Basic update script, used to clone target repos into the `repos/` directory. The target repos will be deleted after processing by `processing.py`. 

### `processing.py`

Basic processing script, used to process files of interest in target repos cloned into the `repos/` directory.

The information obtained from processing the target repos will be put into the `repos_info` directory. 

The target repos will be deleted after processing.  