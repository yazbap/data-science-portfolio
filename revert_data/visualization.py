import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def plot_seniority(non_ab_ba_seniorities, ab_ba_seniorities):
    """
    Plots a histogram for reverts that are part of AB-BA 
    motifs on top of a histogram for all other reverts

    Parameters:
    non_ab_ba_sequences (list): list of seniority differences for all other reverts
    ab_ba_sequnces (list): list of seniority differences for ab-ba reverts
    """

    plt.hist(non_ab_ba_seniorities, bins=50, edgecolor='k', alpha=0.65, label = "All Other Reverts")

    plt.hist(ab_ba_seniorities, bins=50, edgecolor='k', alpha=0.65, label='AB-BA Sequences')

    plt.xlabel('Difference in seniority')

    plt.ylabel('Number of reverts')

    plt.title('Reversion Behavior on Romanian Wikipedia')

    plt.legend()

    plt.yscale('log')

    plt.minorticks_off()

    plt.gca().get_yaxis().set_major_formatter(ScalarFormatter(useMathText=False))

    plt.ylim(1, 1000)

def print_network_data(revert_data):
    '''
    Prints the number of nodes and edges in the network
    and the first 5 data points, a new line for each one
    '''
    nodes_count = set()

    for reverter, reverted_data in revert_data.items():
        nodes_count.add(reverter)
        
        for item in reverted_data:
            nodes_count.add(item['reverted'])

    edges_count = 0

    for key in revert_data:
        edges_count += len(revert_data[key])

    print("The first 5 data points are:")
    first_key, first_values = next(iter(revert_data.items()))
    print(f"{first_key}:")
    for item in first_values[:5]:
        print("\t" + str(item))

    #print the number of nodes and edges
    print("\nThe number of nodes in the network are: " + str(len(nodes_count)))
    print("The number of edges in the network are: " + str(edges_count))