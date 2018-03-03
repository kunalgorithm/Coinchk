from apiserver.settings import github_object

from datetime import datetime
import requests

LIMIT = 5


def get_repo(coin_name):
    return github_object.get_repo(coin_name)


def get_num_stars(repo):
    return repo.stargazers_count


def get_num_branches(repo):
    return len(list(repo.get_branches()))


def get_num_forks(repo):
    return repo.forks_count


def get_num_watchers(repo):
    return repo.watchers_count


def get_readme_content_and_lineno(repo):
    try:
        readme = repo.get_readme()
        download_url = readme.raw_data['download_url']
        readme_raw_text = requests.get(download_url).text.split("\n")
    except:
        return None, 0
    return readme_raw_text, len(readme_raw_text)


def get_commits_and_contributors(repo):
    commits = repo.get_commits()
    contributors_data = {}
    commits_data = []
    commit_id = 0
    for commit in commits:
        c_stats = commit.stats
        if commit.author is None:
            continue
        author_name = commit.author.login
        num_lines_added = c_stats.additions
        num_lines_deleted = c_stats.deletions
        commit_date = datetime.strptime(c_stats.last_modified, "%a, %d %b %Y %X GMT").strftime('%Y-%m-%d')

        if author_name not in contributors_data:
            contributors_data[author_name] = {
                'num_lines_added': 0,
                'num_commits': 0,
                'num_lines_deleted': 0,
                'num_lines_edited': 0
            }

        commits_data.append(
            {
                'id': commit_id,
                'date': commit_date,
                'num_lines_added': num_lines_added,
                'num_lines_deleted': num_lines_deleted,
                'num_lines_edited': num_lines_added + num_lines_deleted
            }
        )

        contributors_data[author_name]['num_lines_added'] += num_lines_added
        contributors_data[author_name]['num_commits'] += 1
        contributors_data[author_name]['num_lines_deleted'] += num_lines_deleted
        contributors_data[author_name]['num_lines_edited'] += (num_lines_added + num_lines_deleted)

        commit_id += 1
        if commit_id >= LIMIT:
            break

    contributors = []
    contributor_id = 0
    for k, v in contributors_data.iteritems():
        contributors.append(
            {
                'author_name': k,
                'id': contributor_id,
                'num_commits': v['num_commits'],
                'num_lines_added': v['num_lines_added'],
                'num_lines_deleted': v['num_lines_deleted'],
                'num_lines_edited': v['num_lines_edited'],
            }
        )
        contributor_id += 1

    contribs_stats = repo.get_stats_contributors()
    if contribs_stats is None: contribs_stats = repo.get_stats_contributors()
    cnt = 0 if contribs_stats is None else len(contribs_stats)
    return {"num_commits": commit_id, "commits": commits_data}, {"num_contributors": cnt, "contributors": contributors}


def get_pull_requests(repo):
    open_prs = repo.get_pulls()
    closed_prs = repo.get_pulls('closed')

    prs = {}
    prs_data = {}

    pr_id = 0
    open_pr_counts = 0
    closed_pr_counts = 0
    for pr in open_prs:
        prs_data[pr_id] = {
            'title': pr.title,
            'date': pr.updated_at.strftime("%Y-%m-%d"),
            'internal_id': pr.number,
            'open': True
        }
        pr_id += 1
        open_pr_counts += 1
        if open_pr_counts >= LIMIT:
            break

    for pr in closed_prs:
        prs_data[pr_id] = {
            'title': pr.title,
            'date': pr.updated_at.strftime("%Y-%m-%d"),
            'internal_id': pr.number,
            'open': False
        }
        pr_id += 1
        closed_pr_counts += 1
        if closed_pr_counts >= LIMIT:
            break

    prs['num_prs_open'] = open_pr_counts
    prs['num_prs_closed'] = closed_pr_counts
    prs['prs'] = prs_data
    return prs


def get_issues(repo):
    open_issues = repo.get_issues()
    closed_issues = repo.get_issues(state='closed')

    issues = []
    issues_data = {}

    issue_id = 0
    open_issue_count = 0
    closed_issue_count = 0
    for issue in open_issues:
        issues.append(
            {
                'title': issue.title,
                'id': issue_id,
                'date': issue.created_at.strftime('%Y-%m-%d'),
                'open': 1
            }
        )
        open_issue_count += 1
        issue_id += 1
        if open_issue_count >= LIMIT:
            break

    for issue in closed_issues:
        issues.append(
            {
                'title': issue.title,
                'id': issue_id,
                'date': issue.created_at.strftime('%Y-%m-%d'),
                'open': 0
            }
        )
        closed_issue_count += 1
        issue_id += 1
        if closed_issue_count >= LIMIT:
            break

    # issues_data['num_issues_open'] = open_issue_count
    issues_data['num_issues_open'] = repo.open_issues_count
    issues_data['num_issues_closed'] = closed_issue_count
    issues_data['issues'] = issues

    return issues_data


def get_fork_and_addr(repo):
    return 1 if repo.fork else 0


def get_coin_data(name, id, rank):
    repo = get_repo(id)
    res = {}

    res["name"] = name
    res["rank"] = rank
    res["id"] = id
    res["num_stars"] = get_num_stars(repo)
    res["num_branches"] = get_num_branches(repo)
    res["num_forks"] = get_num_forks(repo)
    res["num_watchers"] = get_num_watchers(repo)

    readme, num_lines = get_readme_content_and_lineno(repo)
    if readme is not None:
        res["readme_exists"] = 1
        res["readme_linecount"] = num_lines
    else:
        res["readme_exists"] = 0
        res["readme_linecount"] = 0

    commits, contributors = get_commits_and_contributors(repo)
    res.update(commits)
    res.update(contributors)

    prs = get_pull_requests(repo)
    res.update(prs)
    issues = get_issues(repo)
    res.update(issues)

    res['forked'] = get_fork_and_addr(repo)

    return res
