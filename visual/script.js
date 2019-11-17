var config = {
                container_id: "viz",
                server_url: "bolt://localhost:7687",
                server_user: "neo4j",
                server_password: "neo4j",
                labels: {
                    "User": {
                        caption: "name",
                        size: "in_degree",
                        community: "community"
                    }
                },
                relationships: {
                    "FOLLOW": {
                        thickness: 0.03,
                        caption: false
                    }
                },
                arrows: true,
                initial_cypher: "MATCH p=(u1:User)-[]-(u2:User) WHERE u1.in_degree > 10  RETURN p"
            }

var viz;

function draw() {
     viz = new NeoVis.default(config);
     viz.render();
}
