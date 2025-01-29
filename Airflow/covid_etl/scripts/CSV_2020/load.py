from confluent_kafka import Producer
import json


def load_recods(records):
    producer = Producer({'bootstrap.servers': 'kafka:9092'})

    for message in records:
        producer.poll(0)
        producer.produce('etl', value=json.dumps(message))

    producer.flush()
