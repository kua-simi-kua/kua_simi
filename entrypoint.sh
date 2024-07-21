#!/bin/bash

token=$1

cd ./scripts/ && python ./auth_repo_metadata_pull.py ../config/repos_list_dir/repos_list_1.json -t $1
