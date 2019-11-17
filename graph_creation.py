from neo4j import GraphDatabase
import json
import os

def get_driver():
    return GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))

driver = get_driver()
dir = './scrape'

def add_user(tx, name, friend_list):
    tx.run("MERGE (u1:Random:User {name: $name}) "
           "WITH u1 "
           "UNWIND $friend_list AS friend "
           "MERGE (u2:User {name: friend}) "
           "CREATE (u1)<-[:MENTION]-(u2) ",
           name=name, friend_list=friend_list)

def add_friend(tx, name, friend_list):
    tx.run("MERGE (u1:Random:User {name: $name}) "
           "WITH u1 "
           "UNWIND $friend_list AS friend "
           "MERGE (u2:User {name: friend}) "
           "CREATE (u1)-[:FRIEND]->(u2) ",
           name=name, friend_list=friend_list)

def main():
    files = os.listdir(dir)
    for file in files:
        print(file)
        with open(dir + '/' + str(file), 'r') as f:
            datastore = json.load(f)
            with driver.session() as session:
                for user, friends_list in datastore.items():
                    session.write_transaction(add_user, user, friends_list)
                    #session.write_transaction(add_friend, user, datastore.keys())

if __name__ == "__main__":
    main()
