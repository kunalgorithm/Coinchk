from apiserver.settings import github_object

import datetime
import requests


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
    readme = repo.get_readme()
    download_url = readme.raw_data['download_url']
    readme_raw_text = requests.get(download_url).text.split("\n'")
    return readme_raw_text, len(readme_raw_text)


def get_commits_and_contributors(repo):
    commits = repo.get_commits()

    contributors_data = {}
    commits_data = {}
    commit_id = 0
    for commit in commits[::-1]:
        c_stats = commit.stats
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

        commits_data[commit_id] = {
            'date': commit_date,
            'num_lines_added': num_lines_added,
            'num_lines_deleted': num_lines_deleted,
            'num_lines_edited': num_lines_added + num_lines_deleted
        }

        contributors_data[author_name]['num_lines_added'] += num_lines_added
        contributors_data[author_name]['num_commits'] += 1
        contributors_data[author_name]['num_lines_deleted'] += num_lines_deleted
        contributors_data[author_name]['num_lines_edited'] += (num_lines_added + num_lines_deleted)

    return commits_data, contributors_data
