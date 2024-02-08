#!/bin/bash 

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <repository_url>"
    exit 1
fi

# Set the URL of the Git repository
repo_url=$1
echo $repo_url

# Get the name of the repo from the url
dirname=${repo_url##*/}

# Set the destination directory where you want to clone the repository
destination_dir="../repos/${dirname}"

# Clone the repository
git clone "$repo_url" "$destination_dir"

# Check if the clone was successful
if [ $? -eq 0 ]; then
    echo "Repository cloned successfully"
else
    echo "Failed to clone repository"
fi

