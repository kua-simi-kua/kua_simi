# KUA SIMI

Current progress:
1. Current `scripts/update.sh` can clone a repo into a directory under the `repos/` directory. User can simply run the command `bash scripts/update.sh REPO_URL` e.g. `bash scripts/update.sh  https://github.com/projectdiscovery/interactsh`

Future work: 
1. Make README more readable
2. Populate the directories. Currently can't push empty directories - there are actually more directories i.e. `repos` to store repositories; `repos_info` to store information about the repos such as file hashes / potential IOCs; `config` to store configurations e.g. json schema for the info we want to store and crontab config
3. Dangerous to clone a repo into `repos/` - this kua_simi repository will not contain contents of the embedded repository, therefore impossible to push updates to the remote on GitHub. Possible solutions would be to only store commit hash s and branches, etc. Will look into this. 
