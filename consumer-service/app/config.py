import os

class Settings:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
    KAFKA_TOPIC = os.getenv("TOPIC_NAME")
    ES_HOST = os.getenv("ES_HOST")
    ES_INDEX = os.getenv("ES_INDEX")

settings = Settings()