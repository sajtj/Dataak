from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from .elastic import ESClient

app = FastAPI()
es_client = ESClient()

class TagRequest(BaseModel):
    doc_id: str
    tag: int

@app.get("/search")
async def search(
    name: str = None,
    username: str = None,
    category: str = None,
    text: str = None
):
    query_params = {
        'Name': name,
        'Username': username,
        'Category': category,
        'Text': text
    }
    try:
        results = es_client.search(query_params)
        return [hit['_source'] for hit in results['hits']['hits']]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))