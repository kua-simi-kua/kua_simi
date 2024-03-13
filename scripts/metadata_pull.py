from github import Github
from argparse import ArgumentParser

def get_repo_string_from_url(repo_url):
    repo_url_token_list = repo_url.split("/")
    repo_string = repo_url_token_list[-2] + '/' + repo_url_token_list[-1]
    return repo_string

def main():
    # starList = repo.get_stargazers_with_dates()
    # print("starList; ")
    # for starPage in starList:
    #     print(starPage)

    # forkList = repo.get_forks()
    # print("forkList: ")
    # for forkPage in forkList:
    #     print(forkPage)

    argparser = ArgumentParser(description="Pull GitHub metadata of a given repo")
    argparser.add_argument("repo_url", help="GitHub URL of the repo")

    args = argparser.parse_args()
    repo_string = get_repo_string_from_url(args.repo_url)


    g = Github()
    print("rate_limit: ", g.get_rate_limit())
    repo = g.get_repo(repo_string)

    print("forks_count: ", repo.forks_count)
    print("stars:", repo.stargazers_count)
    print("forks_url: ", repo.forks_url)
    
if __name__ == "__main__":
    main()