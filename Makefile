run:
	python3 -m scraper.scrape

neo4j:
	docker-compose up -d neo4j
	docker-compose logs -f neo4j