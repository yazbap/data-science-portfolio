from datetime import datetime
import math
import seniority_processing

TIME_INDEX = 0
REVERT_INDEX = 1
VERSION_INDEX = 2
NAME_INDEX = 3

def parse_content(file_path):
    '''
    Parses the content of the file and returns a list of lists.

    Parameters:
    file_path (str): The path to the file to be parsed.

    Returns:
    content (list): A list of lists containing the parsed content.
    '''
    with open(file_path) as f:
        next(f)  # skip header
        content = [x.strip().split()[1:] for x in f]

    for element in content:
        element[0] = datetime.strptime(' '.join(element[:2]), "%Y-%m-%d %H:%M:%S")
        element[1:] = element[2:]
        element[2] = int(element[VERSION_INDEX])

    return content

def process_edit_data(content_sorted):
    '''
    Processes the edit data to find the seniority of each editor at each edit.
    
    Parameters:
    content_sorted (list): A list of lists containing the parsed content, sorted by time.
    
    Returns:
    edit_dic (dict): A dictionary containing the seniority of each editor at each edit.
    '''
    edit_count = {}
    edit_dic = {}

    for edit in content_sorted:
        name = edit[NAME_INDEX]
        # Set the edit count of the editor starting from 1
        edit_count[name] = edit_count.get(name, 0) + 1
        seniority = math.log(edit_count[name],10)
        edit_dic.setdefault(name, []).append({'time': edit[TIME_INDEX], "seniority": seniority})

    return edit_dic

def find_revert_data(content, potential_reverts, edit_dic, max_num_versions):
    '''
    Finds the revert data for each potential revert.

    Parameters:
    content (list): A list of lists containing the parsed content.
    potential_reverts (list): A list of lists containing the potential reverts.
    edit_dic (dict): A dictionary containing the seniority of each editor at each edit.
    max_num_versions (int): The maximum number of versions to consider for a revert.

    Returns:
    revert_data (dict): A dictionary containing the revert data for each potential revert.
    '''
    revert_data = {}

    for potential_revert in potential_reverts:
        max_num_iterations = content.index(potential_revert) + (max_num_versions - potential_revert[VERSION_INDEX])

        for i in range(content.index(potential_revert) + 1, max_num_iterations):
            if content[i][VERSION_INDEX] == potential_revert[VERSION_INDEX]:
                potential_reverted = content[i - 1]

                if potential_reverted[NAME_INDEX] == potential_revert[NAME_INDEX]:
                    break  # not a valid revert, continue to the next potential_revert
                else:  # Valid revert found
                    revert_data = process_revert_data(potential_revert, potential_reverted, edit_dic, revert_data)
                    break  # revert found, continue to the next potential_revert

    return revert_data

def process_revert_data(potential_revert, potential_reverted, edit_dic, revert_data):
    '''
    Processes the revert data for a potential revert and potential reverted edit.

    Parameters:
    potential_revert (list): A list containing the potential revert.
    potential_reverted (list): A list containing the potential reverted edit.
    edit_dic (dict): A dictionary containing the seniority of each editor at each edit.
    revert_data (dict): A dictionary containing the revert data for each potential revert.

    Returns:
    revert_data (dict): A dictionary containing the revert data for each potential revert.
    '''
    revert_seniority_data = edit_dic[potential_revert[NAME_INDEX]]
    reverted_seniority_data = edit_dic[potential_reverted[NAME_INDEX]]

    reverter_entry = next(edit for edit in revert_seniority_data if edit['time'] == potential_revert[TIME_INDEX])
    reverted_entry = next(edit for edit in reverted_seniority_data if edit['time'] == potential_reverted[TIME_INDEX])

    revert_data.setdefault(potential_revert[NAME_INDEX], []).append({
        'reverted': potential_reverted[NAME_INDEX],
        'time': potential_revert[TIME_INDEX],
        'seniority_reverter': reverter_entry['seniority'],
        'seniority_reverted': reverted_entry['seniority']
    })

    return revert_data

def process_reverter(reverter_key, reverter_data, revert_data, ab_ba_seniorities, considered_reverts):
    '''
    Processes the reverts conducted by a reverter and finds AB-BA seniorities.

    Parameters:
    reverter_key (str): The name of the reverter.
    reverter_data (list): A list containing the revert data for the reverter.
    revert_data (dict): A dictionary containing the revert data for each potential revert.
    ab_ba_seniorities (list): A list containing the AB-BA seniorities.
    considered_reverts (list): A list containing the considered reverts.

    Returns:
    ab_ba_seniorities (list): A list containing the AB-BA seniorities.
    considered_reverts (list): A list containing the considered reverts.
    '''
    for revert in reverter_data:
        if revert['reverted'] in revert_data:
            reverted = revert['reverted']
            for entry in revert_data[reverted]:
                seniority_processing.find_ab_ba_seniorities(entry, revert, ab_ba_seniorities, reverter_key, considered_reverts)

def process_all_revert_data(revert_data):
    '''
    Processes all reverter data to find AB-BA seniorities.

    Parameters:
    revert_data (dict): A dictionary containing the revert data for each potential revert.

    Returns:
    ab_ba_seniorities (list): A list containing the AB-BA seniorities.
    considered_reverts (list): A list containing the considered reverts.
    '''
    ab_ba_seniorities = list()
    considered_reverts = list()

    for reverter_key, reverter_data in revert_data.items():
        process_reverter(reverter_key, reverter_data, revert_data, ab_ba_seniorities, considered_reverts)

    return ab_ba_seniorities, considered_reverts