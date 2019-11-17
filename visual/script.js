var config = {
                container_id: "viz",
                server_url: "bolt://51.143.173.230:7687",
                server_user: "neo4j",
                server_password: "neo4j",
                labels: {
                    "User": {
                        caption: "name"
                        /*size: "in_degree",
                        community: "community"*/
                    }
                },
                relationships: {
                    "MENTION": {
                        thickness: 0.03,
                        caption: false
                    }
                },
                arrows: true,
                initial_cypher: "MATCH p=(u1:User)-[:MENTION]->(u2:User) RETURN p LIMIT 20"
            }

var viz;

function draw() {
     viz = new NeoVis.default(config);
     viz.render();
}
