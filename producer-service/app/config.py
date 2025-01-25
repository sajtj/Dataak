import os

class Settings:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
    KAFKA_TOPIC = os.getenv("TOPIC_NAME")
    API_URL = os.getenv("API_URL")

settings = Settings()