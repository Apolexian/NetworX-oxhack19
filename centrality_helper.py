import networkx as nx
import pandas as pd


def get_network_degree_centrality(G):
    return pd.Series(nx.degree_centrality(G)).sort_values(ascending=False)


