# Dataak
# Text Data Pipeline with Kafka, Elasticsearch, and FastAPI

## Architecture
1. Producer Daemon: Fetches data from API every minute and sends to Kafka
2. Consumer Daemon: Consumes data from Kafka and indexes to Elasticsearch
3. FastAPI Service: Provides search capabilities

## Services
- Kafka: Message broker
- Elasticsearch: Search engine
- Producer: Data ingestion service
- Consumer: Data indexing service
- FastAPI: API service

## API Endpoints
- GET /search?name=&username=&category=&text=

## Run the system
```bash
docker compose up --build
