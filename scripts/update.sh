#!/bin/bash 

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <repository_url>"
    exit 1
fi

# Set the URL of the Git repository
repo_url=$1
echo $repo_url

# Extract the username and repository name from the URL
# Note: This assumes that the repository URL follows the standard GitHub format, such as https://github.com/username/repo.git.
# If your repositories are hosted elsewhere, you may need to adjust the script accordingly.
repo_url="$1"
IFS='/' read -r -a parts <<< "$repo_url"
USERNAME="${parts[3]}"
REPO_NAME="${parts[4]}"

# Set the destination directory where you want to clone the repository
destination_dir="../repos/${REPO_NAME}"

# Create destination directory if it doesn't exist
mkdir -p "$destination_dir"
echo "Destination Directory: $destination_dir"

# Clone the repository
git clone "$repo_url" "$destination_dir"

# Check if the clone was successful
if [ $? -eq 0 ]; then
    echo "Repository cloned successfully"
else
    echo "Failed to clone repository"
fi