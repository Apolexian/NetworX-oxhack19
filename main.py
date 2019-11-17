import pandas as pd
import numpy as np
import os
from tweepy import OAuthHandler, API, TweepError
from oxhack.political_eng_converter import extract_account_engagement, intersection

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)
def parse_json_to_dict(filename):
    with open(filename) as f:
        data = json.load(f)
        f.close()
    return data
G = nx.DiGraph()
files = os.listdir('scraped_accounts')
core_users = []
link_users = []
political_engagement = {}
for file in files[:10]:
    users = parse_json_to_dict(f'scraped_accounts/{file}')
    core_users.append(list(users.keys())[0])
    link_users.extend(list(users.keys()))
    G.add_nodes_from(users.keys())
    for k, v in users.items():
        G.add_edges_from(([(k, t) for t in v]))
print(nx.info(G))
centrality = nx.pagerank(G)
central_nodes = list(pd.Series(centrality).sort_values(ascending=False).index)[:10]
central_nodes_eng = extract_account_engagement(central_nodes, auth_api)
political_engagement.update(central_nodes_eng)
for node in G.nodes():
    if node not in link_users:
        political_engagement[node] = 0
    elif node in link_users and node not in core_users:
        neighbours = [connection for connection in iter(G[node])]
        central_neighbours = intersection(neighbours, central_nodes)
        pe_score = 0
        for c_neighbour in central_neighbours:
            pe_score += political_engagement[c_neighbour] / len(central_neighbours)
        political_engagement[node] = np.round(pe_score, 3)
for node in G.nodes():
    if node in core_users:
        neighbours = [connection for connection in iter(G[node])]
        neighbours = list(set(neighbours).difference(set(core_users)))
        best_friends = intersection(neighbours, link_users)
        other_friends = intersection(list(set(neighbours).difference(set(link_users))), central_nodes)
        pe_score = 0
        for bf in best_friends:
            pe_score += 0.5 * political_engagement[bf] / len(best_friends)
        for of in other_friends:
            pe_score += 0.5 * political_engagement[of] / len(other_friends)
        political_engagement[node] = pe_score

nx.set_node_attributes(G, political_engagement, "political_engagement")
print(pd.Series(political_engagement).sort_values(ascending=False))

reps = ["RepAdamSchiff", "DonaldJTrumpJr", "POTUS", "GOP", "GOPLeader", "FoxNews", "GOPChairwoman", "WhiteHouse", "IvankaTrump", "LevinTV", "Jim_Jordan", "EliseStefanik", "senatemajldr", "DevinNunes", "EddieRispone", "paulsperry_"]
dems = ['AOC', 'MSNBC', 'SpeakerPelosi', 'nytimes', 'RepMarkMeadows', 'washingtonpost', 'BernieSanders', 'thehill', 'TedraCobb', 'CNN', 'sbg1', 'RepStefanik', 'NBCNews', 'HillaryClinton', 'PeteButtigieg', 'AndrewYang']
pol_affiliation = {}
for node in G.nodes():
    if node in reps:
        pol_affiliation[node] = 1
    elif node in dems:
        pol_affiliation[node] = -1
    else:
        neighbours = [connection for connection in iter(G[node])]
        l = intersection(neighbours, dems)
        r = intersection(neighbours, reps)
        if l > r:
            dems.append(node)
            pol_affiliation[node] = -1
        else:
            reps.append(node)
            pol_affiliation[node] = 1