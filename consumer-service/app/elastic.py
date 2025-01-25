from elasticsearch import Elasticsearch
from app.config import settings
import datetime
import time

class ESClient:

    def __init__(self, es_host):
        self.es = Elasticsearch(
            [es_host],
            max_retries=5,
            retry_on_timeout=True,
            request_timeout=30
        )
        self._wait_for_connection()
        self.index_name = settings.ES_INDEX
        self._create_index()


    def _wait_for_connection(self):
        for _ in range(10):
            try:
                if self.es.ping():
                    return
                time.sleep(5)
            except Exception:
                time.sleep(5)
        raise ConnectionError("Could not connect to Elasticsearch")

    def _create_index(self):
        if not self.es.indices.exists(index=self.index_name):
            mapping = {
                "mappings": {
                    "properties": {
                        "Name": { "type": "text" },         # Text type for Title
                        "Username": { "type": "keyword" },  # Keyword for Author
                        "Category": { "type": "keyword" },  # Keyword for Genre
                        "Text": { "type": "text" },         # Text type for Content
                        "inserted_at": { "type": "date" }   # Timestamp
                    }
                }
            }
            self.es.indices.create(index=self.index_name, body=mapping)

    def index_document(self, kafka_doc):
        es_doc = {
            "Name": kafka_doc.get("title"),           # Title → Name (text)
            "Username": kafka_doc.get("author"),      # Author → Username (keyword)
            "Category": kafka_doc.get("genre"),       # Genre → Category (keyword)
            "Text": kafka_doc.get("content"),         # Content → Text (text)
            "inserted_at": datetime.datetime.now()    # Add timestamp
        }
        
        self.es.index(index=self.index_name, body=es_doc)