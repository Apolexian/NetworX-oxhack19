from neo4j import GraphDatabase
import json
import os

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))
dir = './scrape'

def add_user(tx, name, friend_name):
    tx.run("MERGE (u1:User {name: $name}) "
           "WITH u1 "
           "UNWIND $friend AS friend "
           "MERGE (u2:User {name: friend}) "
           "CREATE (u1)<-[:METION]-(u2) ",
           name=name, friend=friend_name)

def main():
    files = os.listdir(dir)
    for file in files:
        with open(dir + '/' + str(file), 'r') as f:
            datastore = json.load(f)
            with driver.session() as session:
                for user, friends_list in datastore.items():
                    print(user)
                    session.write_transaction(add_user, user, friends_list)

if __name__ == "__main__":
    main()