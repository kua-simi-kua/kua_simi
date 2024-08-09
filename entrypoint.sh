#!/bin/bash

token=$1
file_path=$2

cd ./scripts/ && python ./auth_repo_metadata_pull.py $2 -t $1
