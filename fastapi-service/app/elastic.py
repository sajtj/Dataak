from elasticsearch import Elasticsearch
from app.config import settings


class ESClient:
    def __init__(self):
        self.es = Elasticsearch([settings.ES_HOST])
        self.index_name = settings.ES_INDEX

    def search(self, query_params):
        must_clauses = []
        for field, value in query_params.items():
            if value and field in ['Name', 'Username', 'Category', 'Text']:
                must_clauses.append({"match": {field: value}})
        
        body = {
            "query": {
                "bool": {
                    "must": must_clauses
                }
            }
        }
        return self.es.search(index=self.index_name, body=body)