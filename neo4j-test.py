from dump_file import users
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))

def add_user(tx, name, friend_name):
    tx.run("MERGE (u1:User {name: $name}) "
           "WITH u1 "
           "UNWIND $friend AS friend "
           "MERGE (u2:User {name: friend}) "
           "CREATE (u1)-[:FOLLOW]->(u2) ",
           name=name, friend=friend_name)

with driver.session() as session:
    for user, friends_list in users.items():
        session.write_transaction(add_user, user, friends_list)

