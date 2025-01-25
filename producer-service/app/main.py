from app.producer import DataProducerDaemon

if __name__ == "__main__":
    producer = DataProducerDaemon()
    producer.run()