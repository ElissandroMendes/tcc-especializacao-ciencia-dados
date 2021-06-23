import json
import threading

from kafka import KafkaConsumer, KafkaProducer


class Consumer(threading.Thread):

    def run(self):
        print("Creating Consumer instance")
        stream = KafkaConsumer(bootstrap_servers='localhost:9092',
                               auto_offset_reset='latest',
                               value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        print("Subscribe to Topic")
        stream.subscribe(['sensor-data'])
        print("Pooling message")
        for message in stream:
            print(f'From [ {message.topic} ] -> {message.value}')


if __name__ == '__main__':
    threads = [
        Consumer()
    ]

    for t in threads:
        t.start()