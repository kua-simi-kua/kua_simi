# KUA SIMI

*"Kua"* = Hokkien for "look"/"see"

*"simi"* = Hokkien for "what"

*"Kua simi?!* = "What are you looking at?!"

This project looks into tracking OffSec tools that may be used for malicious purposes, through the use of 
1. monitoring changes in tools of interest and 
2. monitoring changes in interest in tools

### Quick Start Guide and Setup:
1. Install required libraries (list below will be updated as the project progresses):
```
pip install pygithub
```
2. Clone this repository.

### Monitoring Changes in Tools of Interest 

### Monitoring Changes in Interest in Tools

This is largely done by pulling metadata from the target GitHub repositories, which are specified in `config/repos_list.json`. 

Currently `scripts/metadata_pull.py` takes in `config/repos_list.json` as an argument, and for each target repo specified, pulls the counts of GitHub stars and forks. This metadata gets appended into a json file for each target repo, listed in `repos_info/metadata/`. 

To run the script, navigate into the `scripts/` directory and run the following command:
```
python metadata_pull.py ../config/repos_list.json
```

and then navigate into `repos_info/metadata/` to examine the resulting metadata.


## Changelog:
(As this gets longer, will shift to a new `.md` file)

`2024-03-20`: `metadata_pull.py` can pull metadata (fork count and star count) from target github repos, and create new json files for these metadata / append these metadata to existing json files. These target github repos are specified in `/config/repos_list.json`.

`2024-02-19`: `processing.py` script now stores time of hash extraction along with hash in the json files in `repos_info`. `compare.py` script is able to compare the new and old json files in `repos_info`, detect changes the newer json file has from the older json file and then append these differences into the older json file. Following which, it then deletes the newer json file. 

`2024-02-14`: Added merge request into new feature branch. Tweaked update.sh script, functionality is still the same. Added processing.py script, currently able to process the SHA256 hashes of .py/.sh files in the repos clone via update.sh.

`2024-02-08`: Populate the directories. Currently can't push empty directories - there are actually more directories i.e. `repos` to store repositories; `repos_info` to store information about the repos such as file hashes / potential IOCs; `config` to store configurations e.g. json schema for the info we want to store and crontab config

`2024-01-25`: Current `scripts/update.sh` can clone a repo into a directory under the `repos/` directory. User can simply run the command `bash scripts/update.sh REPO_URL` e.g. `bash scripts/update.sh  https://github.com/projectdiscovery/interactsh`

## Future work: 
(As this gets longer, will shift to a new `.md` file or possibly track via Issues)

1. Dangerous to clone a repo into `repos/` - this kua_simi repository will not contain contents of the embedded repository, therefore impossible to push updates to remote repo. Possible solution to clone --> process --> delete

2. Add other files of interest for `processing.py` to process

3. Pull additional metadata e.g.
    a. List out contributors of interest for each target repo (seems like not possible through GitHub api, may need to resort to cloned repo)
    b. Get the top `n` popular files/paths of each target repo 
    c. Get number of `git clone` and views over the past `n` days for each target repo

4. Abstract out common helper functions into `scripts/utils` e.g. helper functions to read and write from json config files and files containing metadata and hashes
