from confluent_kafka import Producer
import time
import requests
import json
from app.config import settings

class FakerAPIClient:
    API_URL = settings.API_URL
    
    def fetch_data(self):
        response = requests.get(self.API_URL)
        response.raise_for_status()
        return response.json()['data']


class KafkaProducerClient:

    def __init__(self, bootstrap_servers: str, topic: str):
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers
        })
        self.topic = topic

    def send_message(self, data: dict):
        try:
            self.producer.produce(
                topic=self.topic,
                value=json.dumps(data).encode('utf-8')
            )
            self.producer.flush()
            
        except Exception as e:
            print(f"Failed to send message: {e}")



class DataProducerDaemon:
    
    def __init__(self):
        self.api_client = FakerAPIClient()
        self.producer = KafkaProducerClient(
            bootstrap_servers=settings.KAFKA_BROKER,
            topic=settings.KAFKA_TOPIC
        )
    
    def run(self):
        while True:
            try:
                data = self.api_client.fetch_data()
                for record in data:
                    self.producer.send_message(record)
                print(f"Sent {len(data)} records to Kafka")
                time.sleep(60)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(10)