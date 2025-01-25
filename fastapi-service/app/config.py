import os

class Settings:
    ES_HOST = os.getenv("ES_HOST")
    ES_INDEX = os.getenv("ES_INDEX")

settings = Settings()