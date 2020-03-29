import git


def branchname():
    repo = git.Repo(search_parent_directories=True)
    branch = repo.active_branch
    return branch.name
