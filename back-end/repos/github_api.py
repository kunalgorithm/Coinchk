from apiserver.settings import g


def get_contributors(req):

    repo_name = req.get_repo_id()
    repo = g.get_repo(repo_name)

    l = []

    return l
