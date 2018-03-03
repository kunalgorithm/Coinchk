from apiserver.settings import github_object


def get_contributors(req):

    repo_name = req.get_repo_id()
    repo = github_object.get_repo(repo_name)

    l = []

    return l
