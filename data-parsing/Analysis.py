import json
import numpy as np
import math

# Read in the input json data and store in variable data
with open("sample.json", "r") as input_file:
    data = json.load(input_file)
    input_file.close()

CUTOFF = 0.3


# Methods for creating new data parameters from existing ones
# For commits + num days since commit

def average_days():
    for currency_name in data.keys():
        commit_lst = data[currency_name]["commits"]
        for commit in commit_lst:
            data[currency_name]["average days since commits"] += commit["date"]
        data[currency_name]["average days since commits"] \
            = data[currency_name]["average days since commits"] / len(commit_lst)





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
entry_names = ["contributors", "stars"]

#entry_names = ["num_branches", "num_stars", "num_forks", "num_watchers",
#  "num_contributors", "num_branches", "rank", "readme_linecount", "num_commits",
#  "num_prs_open", "num_issues_closed"]


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
        for val in data.keys():
            temp.append(data[val][name])
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
    currency_data = data[currency_name]
    temp = {}
    for name in entry_names:
        if (dict_cutoff[name] < currency_data[name]):
            temp[name] = True
        else:
            temp[name] = False
    return {currency_name: temp}

"""
No inputs, will just repeatedly call specific_currency_home_data
to compute the boolean values based on cutoffs for each of the currencies

@Return
    There is no return, this method will directly convert the dictionary 
    computed into json and write that into the specified file
"""
def all_currency_home_data():
    overall = {}
    dict_cutoff = cutoff_mapping()
    for currency_name in data:
        overall.update(specific_currency_home_data(currency_name, dict_cutoff))
    with open("output_sample.json", "w") as f:
        json.dump(overall, f)
        f.close()

#Get everything started
all_currency_home_data()


#-------------------------------------------------------------------------------------------------
#                               Compute an Aggregated Value for each currency
#-------------------------------------------------------------------------------------------------


def compute_max(lst):
    array = np.array(lst)
    return np.amax(lst)

entry_names = data["bitcoin"].keys()

def field_maxes():
    mapping = {}
    for name in entry_names:
        temp = []
        for val in data.keys():
            temp.append(data[val][name])
        mapping[name] = math.log10(compute_max(temp))
    return mapping

def compute_score(currency_name, max_dict):
    total = 0
    for name in entry_names:
        total += (math.log10(data[currency_name][name]) / max_dict[name])
    return (total * 100) / len(entry_names)

def all_scores():
    final = {}
    max_dict = field_maxes()
    for currency_name in data:
        final[currency_name] = compute_score(currency_name, max_dict)
    with open("total_scores.json", "w") as f:
        json.dump(final, f)
        f.close()


all_scores()
