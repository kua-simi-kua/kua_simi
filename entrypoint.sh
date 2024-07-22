#!/bin/bash

token=$1

cd ./scripts/ && python ./auth_repo_metadata_pull.py ../config/repos_list_long.json -t $1
