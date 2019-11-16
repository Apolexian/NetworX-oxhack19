import networkx as nx
import json

def get_example_network():
    json1_file = open('example_network.json', 'r')
    json1_str = json1_file.read()
    json1_file.close()
    json1_data = json.loads(json1_str)
    return json1_data


def get_network_degree_centrality(network_dict):
    G = nx.DiGraph()
    G.add_nodes_from(network_dict.keys())
    for k, v in network_dict.items():
        G.add_edges_from(([(k, t) for t in v]))
    return nx.degree_centrality(G)

