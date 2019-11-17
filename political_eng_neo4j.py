from neo4j import GraphDatabase
import networkx as nx
import pandas as pd
import extractor
import political_eng_converter

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))
NEO4J_CHUNK = 200

G = nx.DiGraph()


def get_Graph(tx):
    users = {}
    for record in tx.run("MATCH (a:User) "
                         "WITH a "
                         "MATCH (a)-[METION]->(b:User) "
                         "RETURN a.name AS name, collect(b.name) AS friends"):
        users[record['name']] = record['friends']
    return users


def set_pagerank_value(tx, nodes):
    params = []
    for (user, value) in nodes:
        attr = {'name': user, 'value': value}
        params.append(attr)
    tx.run("UNWIND $nodes AS user "
           "MATCH (a:User {name: user.name}) "
           "MATCH (a)<--(n)"
           "WITH user, a, COUNT(n) AS degree "
           "SET a.centrality_degree = user.value, "
           "a.in_degree = degree", nodes=params)


def get_data():
    with driver.session() as session:
        users = session.read_transaction(get_Graph)

    return users


def calculated_pagerank(users):
    G.add_nodes_from(users.keys())
    for k, v in users.items():
        G.add_edges_from(([(k, t) for t in v]))

    return pd.Series(nx.pagerank(G)).sort_values(ascending=False)


def upload_political_eng(political_eng):
    index = 0
    list_nodes = [(k, v) for k, v in nx.pagerank.items()][index:NEO4J_CHUNK]

    while len(list_nodes) > 0:
        with driver.session() as session:
            session.write_transaction(set_political_eng_value, list_nodes)

        index += NEO4J_CHUNK
        list_nodes = [(k, v) for k, v in political_eng.items()][index:index + NEO4J_CHUNK]


def main():
    users = get_data()
    pagerank = calculated_pagerank(users)
    print(pagerank)
    api = extractor.auth()
    # first_users = list(pagerank[:100].keys())
    # print(first_users)
    # political_eng_list = political_eng_converter.extract_account_engagement(first_users,api)
    # print(political_eng_list)
    # upload_pagerank(pagerank[:100])
    # upload_in_degree(in_degree)
    # print(list(nx.dominating_set(G))[0])


if __name__ == "__main__":
    main()
