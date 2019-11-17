from neo4j import GraphDatabase
import networkx as nx

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))
NEO4J_CHUNK = 200

G = nx.DiGraph()


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
           "MATCH (a)<--(n)"
           "WITH user, a, COUNT(n) AS degree "
           "SET a.centrality_degree = user.value, "
           "a.in_degree = degree", nodes=params)


def get_data():
    with driver.session() as session:
        users = session.read_transaction(get_Graph)

        G.add_nodes_from(users.keys())
        for k, v in users.items():
            G.add_edges_from(([(k, t) for t in v]))

        return nx.degree_centrality(G), G.in_degree


def upload_centrality(degree_centrality):
    index = 0
    list_nodes = [(k, v)
                  for k, v in degree_centrality.items()][index:NEO4J_CHUNK]

    while len(list_nodes) > 0:
        with driver.session() as session:
            session.write_transaction(set_centrality_value, list_nodes)

        index += NEO4J_CHUNK
        list_nodes = [(k, v) for k, v in degree_centrality.items()
                      ][index:index + NEO4J_CHUNK]


def main():
    degree_centrality, in_degree = get_data()
    # print(in_degree)
    # upload_centrality(degree_centrality)
    # upload_in_degree(in_degree)
    print(list(nx.dominating_set(G))[0])


if __name__ == "__main__":
    main()
