import json

from kafka import KafkaConsumer

TOPIC_NAME = "event"
KAFKA_SERVER = "localhost:9092"


class LogConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER)
        self.topic = TOPIC_NAME

    def consumable_messages(self):
        self.consumer.subscribe([self.topic])

        try:
            for message in self.consumer:
                yield message.value.decode("UTF-8")
        except KeyboardInterrupt:
            self.consumer.close()


consumer = LogConsumer()

while True:
    for message in consumer.consumable_messages():
        print(message)
