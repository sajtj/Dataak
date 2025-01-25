from confluent_kafka import Consumer, KafkaException
from app.elastic import ESClient
from app.config import settings
import json

class KafkaConsumerClient:

    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BROKER,
            'group.id': 'es-group',
            'auto.offset.reset': 'earliest'
        })
        self.topic = settings.KAFKA_TOPIC
        

    def consume(self):
        self.consumer.subscribe([self.topic])
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                yield json.loads(msg.value().decode('utf-8'))
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()


class DataConsumerDaemon:

    def __init__(self):
        self.kafka_consumer = KafkaConsumerClient()
        self.es_client = ESClient(settings.ES_HOST)
        
    def run(self):
        for message in self.kafka_consumer.consume():
            try:
                self.es_client.index_document(message)
                print(f"Indexed document: {message['title']}")
            except Exception as e:
                print(f"Error indexing document: {str(e)}")