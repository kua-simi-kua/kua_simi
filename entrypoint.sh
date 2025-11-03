#!/bin/bash

file_path=$1
token=$2

cd ./scripts/ && python ./auth_repo_metadata_pull.py $1 -t $2 -dt $3 $4
