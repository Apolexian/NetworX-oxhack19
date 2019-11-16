from neo4j import GraphDatabase
import networkx as nx

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))
NEO4J_CHUNK = 200

def get_Graph(tx):
    users = {}
    for record in tx.run("MATCH (a:User) "
                         "MATCH (a)-[FOLLOW]->(b:User) "
                         "RETURN a.name AS name, collect(b.name) AS friends"):
        users[record['name']] = record['friends']
    return users

def set_centrality_value(tx, nodes):
    params = []
    for (user, value) in nodes:
        attr = {'name': user, 'value': value}
        params.append(attr)
    tx.run("UNWIND $nodes AS user "
           "MATCH (a:User {name: user.name}) "
           "SET a.centrality_degree = user.value ", nodes=params)

with driver.session() as session:
    users = session.read_transaction(get_Graph)
    G = nx.DiGraph()
    G.add_nodes_from(users.keys())
    for k, v in users.items():
        G.add_edges_from(([(k, t) for t in v]))
    d_centrality = nx.degree_centrality(G)

index = 0
list_nodes = [(k, v) for k, v in d_centrality.items()][index:NEO4J_CHUNK]
list_nodes[0]
list_nodes[-1]
while len(list_nodes) > 0:
    with driver.session() as session:
        session.write_transaction(set_centrality_value, list_nodes)

    index += NEO4J_CHUNK
    list_nodes = [(k, v) for k, v in d_centrality.items()][index:index+NEO4J_CHUNK]
