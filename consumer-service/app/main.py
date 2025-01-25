from app.consumer import DataConsumerDaemon

if __name__ == "__main__":
    consumer = DataConsumerDaemon()
    consumer.run()