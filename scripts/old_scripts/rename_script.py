import os

REPOS_INFO_PATH = "../repos_info/auth_metadata/"
GH_MD_STRING = "github_metadata___"

def main():
    for folder in os.listdir(REPOS_INFO_PATH):
        folder_path = REPOS_INFO_PATH + folder + '/'
        for filename in os.listdir(folder_path):
            if GH_MD_STRING in filename:
                old_filename = folder_path + filename
                new_filename = folder_path + filename[18:]
                os.rename(old_filename, new_filename)
                print(f"{old_filename} should be changed to {new_filename}")

if __name__ == "__main__":
    main()