import json
import numpy as np
import math
from datetime import datetime
import zipfile

# Read in the input json data and store in variable data
with open("top_10coins_data.json", "r") as input_file:
    data = json.load(input_file)
    input_file.close()

CUTOFF = 0.2



def average_commit_days(currency_data):
    now = datetime.now()
    commit_lst = currency_data["commits"]
    currency_data["average days since commits"] = 0
    for commit in commit_lst:
        days = (now - datetime.strptime(commit["date"], "%Y-%m-%d")).days
        currency_data["average days since commits"] += days
    if (len(commit_lst) > 0):
        currency_data["average days since commits"] \
            = currency_data["average days since commits"] / len(commit_lst)
    return currency_data["average days since commits"]

def average_pull_request_days(currency_data):
    now = datetime.now()
    prs_lst = currency_data["prs"]
    currency_data["average days since open prs"] = 0
    length = 0
    for prs in prs_lst.values():
        if (prs["open"] == 0):
            length += 1
            days = (now - datetime.strptime(prs["date"], "%Y-%m-%d")).days
            currency_data["average days since open prs"] += days
    if (length > 0):
        currency_data["average days since open prs"] \
            = currency_data["average days since open prs"] / len(prs_lst)
        return currency_data["average days since open prs"]
    else:
        return math.inf






def get_currency_data(currency_name):
    currency_data = None
    for i in range(0, len(data)):
        if (data[i]["name"] == currency_name):
            currency_data = data[i]
            break
    if (not currency_data == None):
        print("error")
    else:
        return currency_data


def is_opensource(currency_data):
    return True


def is_forked(currency_data):
    return currency_data["forked"] == 0

def readme_threshold():
    temp = []
    for i in range(0, 10):
        temp.append(data[i]["readme_linecount"])
    return np.amin(temp)


def readme_valid(currency_data, threshold):
    return currency_data["readme_linecount"] > threshold


#contributors
def team_size(currency_data):
    if (int(currency_data["rank"]) <= 100):
        return currency_data["num_contributors"] >= 30
    elif (int(currency_data["rank"]) > 100 and int(currency_data["rank"]) <= 500):
        return currency_data["num_contributors"] >= 15
    else:
        return currency_data["num_contributors"] >= 5

def developing(currency_data):
    commit_days = average_commit_days(currency_data)
    prs_days = average_pull_request_days(currency_data)
    return commit_days < 60 or prs_days < 14

def open_issues(currency_data):
    if (int(currency_data["rank"]) <= 20):
        return currency_data["num_issues_open"] < 1000
    else:
        return currency_data["num_issues_open"] < 100

def dev_interest(currency_data):
    return {"num stars": currency_data["num_stars"],
            "num forks": currency_data["num_forks"],
            "num watchers": currency_data["num_watchers"]}

def bool_to_binary(state):
    if(state):
        return 1
    else:
        return 0


def parse_home_data(input, output):
    with open(input, "r") as input_file:
        data = json.load(input_file)
        input_file.close()
    overall = {}
    for i in range(0, len(data)):
        currency_data = data[i]
        currency_name = data[i]["name"]
        dictionary = {
            "opensource": bool_to_binary(is_opensource(currency_data)),
            "forked": bool_to_binary(is_forked(currency_data)),
            "contributors": bool_to_binary(team_size(currency_data)),
            "under development": bool_to_binary(developing(currency_data)),
            "open issues": bool_to_binary(open_issues(currency_data)),
            "interest": (dev_interest(currency_data)),
            "readme": bool_to_binary(readme_valid(currency_data, readme_threshold()))
        }
        overall.update({currency_name: dictionary})
    with open(output, "w") as f:
        json.dump(overall, f)
        f.close()


# -------------- END OF BINARY COMPUTATIONS ----------------------------------------#








def compute_max(lst):
    array = np.array(lst)
    return np.amax(lst)


def max_given_key(key, d):
    temp = []
    for i in range(0, len(d)):
        temp.append(d[i][key])
    return compute_max(temp)


def max_lines_edited(d):
    temp = []
    for i in range(0, len(d)):
        total = 0
        for commit in d[i]["commits"]:
            total += commit["num_lines_edited"]
        temp.append(total)
    return compute_max(temp)


def open_source_score(currency_data):
    return 100

def forked_score(currency_data):
    if (currency_data["forked"] == 1):
        return 0
    else:
        return 300

def dev_score(currency_data, max_lines):
    ave_pulls = average_pull_request_days(currency_data)
    ave_commit = average_commit_days(currency_data)
    lines_edited = 0
    for details in currency_data["commits"]:
        lines_edited += details["num_lines_edited"]

    lines_score = (lines_edited / max_lines) * 75
    ave_pulls_score = (ave_pulls * (-0.667)) + 100
    if (ave_pulls_score < 0):
        ave_pulls_score = 0
    ave_commit_score = (ave_commit * (-0.5)) + 75
    if (ave_commit_score < 0):
        ave_commit_score = 0

    return lines_score + ave_pulls_score + ave_commit_score

def contr_score(currency_data, max_contr):
    score = (currency_data["num_contributors"] / max_contr) * 250
    if score > 250:
        return 250
    else:
        return score

def interest_score(currency_data, max_sum):
    sum = currency_data["num_stars"] + currency_data["num_watchers"] + currency_data["num_forks"]
    score = (currency_data["num_contributors"] / max_sum) * 150
    if (score > 150):
        return 150
    else:
        return score

def readme_score(currency_data, max_lines):
    score = (currency_data["readme_linecount"] / max_lines) * 50
    if (score > 50):
        return 50
    else:
        return score

def open_issues_score(currency_data):
    allowance = currency_data["num_issues_open"] - currency_data["num_stars"]
    if (allowance > 0):
        temp = allowance * (-0.5)
        if (temp > -20):
            return 0
        else:
            return 20 - temp
    else:
        return 0



def currencyScores(input, output):
    overall = {}
    potential = 1120
    max_lines, max_contr, max_starts, max_watchers, max_forks, max_readme_line = 0, 0, 0, 0, 0, 0

    with zipfile.ZipFile(input, "r") as input_file:
        for file in input_file.namelist():
            with input_file.open(file) as f:
                data = f.read()
                d = json.loads(data.decode("utf-8"))


            max_lines = max(max_lines_edited(d), max_lines)
            max_contr = max(max_given_key("num_contributors", d), max_contr)
            max_stars = max(max_given_key("num_stars", d), max_starts)
            max_watchers = max(max_given_key("num_watchers", d), max_watchers)
            max_forks = max(max_given_key("num_forks", d), max_forks)
            max_readme_line = max(max_given_key("readme_linecount", d), max_readme_line)

    with zipfile.ZipFile(input, "r") as input_file:
        for file in input_file.namelist():
            with input_file.open(file) as f:
                data = f.read()
                d = json.loads(data.decode("utf-8"))

                for i in range(0, len(d)):
                    currency_data = d[i]
                    currency_name = d[i]["name"]
                    score_attr_1 = open_source_score(currency_data)
                    score_attr_2 = forked_score(currency_data)
                    score_attr_3 = dev_score(currency_data, max_lines)
                    score_attr_4 = contr_score(currency_data, max_contr)
                    score_attr_5 = interest_score(currency_data,
                                                        max_stars
                                                        + max_watchers
                                                        + max_forks)
                    score_attr_6 = readme_score(currency_data, max_readme_line)
                    score_attr_7 = open_issues_score(currency_data)
                    final_score = ((score_attr_1 + score_attr_2 + score_attr_3 +
                                    score_attr_4 + score_attr_5 + score_attr_6 + score_attr_7) / potential) * 100
                    overall.update({currency_name: final_score})
    with open(output, "w") as f:
        json.dump(overall, f)
        f.close()














#-------------------------------------------------------------------------------------
# The Following Is for Home Page Cutoffs, Whatever data sent will be assumed to be
# Significant and it will be analyzed
#-------------------------------------------------------------------------------------

"""
@Parameters
    lst: A list of a numerical values
    threshold: the percentile, below which all values 
    won't be taken (expressed in decimal form).
    If no threshold is specified, the default will be
    the hard-coded cutoff value
    
@Returns
    The numerical value of the input percentile    
"""
def compute_cutoff(lst, threshold = CUTOFF):
    array = np.array(lst)
    lst = np.sort(array, axis=None)
    return lst[int(len(lst) * threshold)]


# automatically get all the child fields of a given currency
# entry_names = ["contributors", "stars"]

entry_names = ["num_branches", "num_stars", "num_forks", "num_watchers",
  "num_contributors", "num_branches", "rank", "readme_linecount", "num_commits",
  "num_prs_open", "num_issues_closed", "average days since commits"]

#hard_thresholds = ("contributors (0 - 100)": 15, "readme": "more than least of top 10", contributors (100 - 500): 10
# contributors (500 - ): 5}

"""
No Inputs

@Return 
    Automatically computes a mapping from all the fields
    for a given currency to their respective cutoffs by
    calling @compute_cutoff
"""
def cutoff_mapping():
    mapping = {}
    for name in entry_names:
        temp = []
        for val in data:
            temp.append(val[name])
        mapping[name] = compute_cutoff(temp)
    return mapping

"""
Given a currency name, this will make a dictionary representing
boolean values for the given currency

@Parameters
    currency_name: The name of the currency for which boolean values
    are to be computed
    
@Return
    A dictionary with the currency name as the top level key and its
    value will be all of the boolean values computed from the cutoffs
    for each of the top level fields in the input dictionary
"""
def specific_currency_home_data(currency_name, dict_cutoff):
    currency_data = None
    for i in range(0, len(data)):
        if (data[i]["name"] == currency_name):
            currency_data = data[i]
            break

    temp = {}
    for name in entry_names:
        if (dict_cutoff[name] < currency_data[name]):
            temp[name] = True
        else:
            temp[name] = False
    temp.update(process_binary_names(currency_data))
    return {currency_name: temp}

binary_names = ["fork", "readme_exists"]

"""
Seperate class for socring a given currencies
binary data
"""
def process_binary_names(currency_data):
    temp = {}
    if (currency_data["forked"] == 1):
        temp["forked"] = False
    else:
        temp["forked"] = True

    if (currency_data["readme_exists"] == 0):
        temp["readme_exists"] = False
    else:
        temp["readme_exists"] = True
    return temp


"""
No inputs, will just repeatedly call specific_currency_home_data
to compute the boolean values based on cutoffs for each of the currencies

@Return
    There is no return, this method will directly convert the dictionary 
    computed into json and write that into the specified file
"""
def all_currency_home_data(output):
    print("out")
    overall = {}
    dict_cutoff = cutoff_mapping()
    for val in data:
        overall.update(specific_currency_home_data(val["name"], dict_cutoff))
    with open(output, "w") as f:
        json.dump(overall, f)
        f.close()






#-------------------------------------------------------------------------------------------------
#                               Compute an Aggregated Value for each currency
#-------------------------------------------------------------------------------------------------

# entry_names = data["bitcoin"].keys()

entry_names = ["num_branches", "num_stars", "num_forks", "num_watchers",
  "num_contributors", "num_branches", "readme_linecount", "num_commits",
  "num_prs_open", "num_issues_closed"]

def field_maxes():
    mapping = {}
    for name in entry_names:
        temp = []
        for val in data:
            temp.append(val[name])
        print(temp)
        mapping[name] = math.log10(compute_max(temp))
    return mapping

def compute_score(currency_name, max_dict):
    currency_data = None
    for i in range(0, len(data)):
        if (data[i]["name"] == currency_name):
            currency_data = data[i]
            break
    total = 0
    for name in entry_names:
        total += (math.log10(currency_data[name]) / max_dict[name])
    return (total * 100) / len(entry_names)

def all_scores():
    final = {}
    max_dict = field_maxes()
    for currency_name in data:
        final[currency_name] = compute_score(currency_name, max_dict)
    with open("total_scores.json", "w") as f:
        json.dump(final, f)
        f.close()














def __init__():
    currencyScores("allJson.zip", "score_output.json")
    parse_home_data("top_10coins_data.json", "top_10coins_data_ouput.json")
    parse_home_data("top11_43_coins_data.json", "top11_43_coins_data_ouput.json")
    parse_home_data("top_44_50_coins_data.json", "top_44_50_coins_data_ouput.json")
    parse_home_data("top_51_100_coins_data.json", "top_51_100_coins_data_ouput.json")
    parse_home_data("top_101_140_coins_data.json", "top_101_140_coins_data_ouput.json")
    parse_home_data("top_141_167_coins_data.json", "top_141_167_coins_data_ouput.json")
    parse_home_data("top_168_200_coins_data.json", "top_168_200_coins_data_ouput.json")



__init__()
