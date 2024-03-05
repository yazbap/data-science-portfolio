from datetime import timedelta

def calculate_seniority_differences(revert):
    '''
    Calculates the senioirty difference between the reverter and reverted

    Parameters:
    revert (dict): Edge from revert_data

    Returns:
    int: The difference in seniority between the reverter and reverted
    '''
    return (abs(revert['seniority_reverter'] - revert['seniority_reverted']))

def get_non_ab_ba_seniorities(revert_data, considered_reverts):
    '''
    Gets the seniority differences for non-ab-ba reverts

    Parameters:
    revert_data (dict): Dictionary of revert data
    considered_reverts (set): Set of considered reverts

    Returns:
    list: List of seniority differences for non-ab-ba reverts
    '''
    differences = list()

    for reverter in revert_data:
        for revert in revert_data[reverter]:
            if revert not in considered_reverts:
                differences.append(calculate_seniority_differences(revert))

    return differences

def find_ab_ba_seniorities(reverted_edge, reverters_edge, ab_ba_seniorities, key, considered_reverts):
    '''
    Finds the seniority differences for AB-BA reverts

    Parameters:
    reverted_edge (dict): Edge from reverted
    reverters_edge (dict): Edge from reverter
    ab_ba_seniorities (list): List of seniority differences for AB-BA reverts
    key (str): Name of reverter
    considered_reverts (list): Set of considered reverts
    '''
    # Find the time difference between the reverted's revert and our reverter's revert
    time_difference = reverted_edge['time'] - reverters_edge['time']

    # Check if: 
        #the time difference is within 24 hours
        #the reverted's edge indicates it is reverting the reverter
        #these reverts have not already been considered
    if (timedelta(0) <= time_difference <= timedelta(hours=24)) and \
        (reverted_edge['reverted'] == key) and \
            (reverters_edge not in considered_reverts) and \
                (reverted_edge not in considered_reverts):
        
        considered_reverts.append(reverters_edge)
        considered_reverts.append(reverted_edge)
        
        ab_ba_seniorities.append(calculate_seniority_differences(reverters_edge))