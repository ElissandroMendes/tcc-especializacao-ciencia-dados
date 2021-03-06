import threading
import datetime
import time

from time import sleep
from json import dumps

from dotenv import dotenv_values

from kafka import KafkaProducer
from kafka import errors 

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


class SensorDataCallback(SubscribeCallback):
    message_ = None
    sink = None

    def presence(self, pubnub, presence):
        pass

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            print("PNStatusCategory.PNUnexpectedDisconnectCategory")

        elif status.category == PNStatusCategory.PNConnectedCategory:
            print("Channel connected. Waiting for messages...")

        elif status.category == PNStatusCategory.PNReconnectedCategory:
            print("PNStatusCategory.PNReconnectedCategory")

        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            print("PNStatusCategory.PNDecryptionErrorCategory")

    def message(self, pubnub, message):
        self.message_ = message.message


class ProducerSensorData(threading.Thread):
    pubnub = None
    callback = None
    producer = None

    sensors = ["probe-28500df7", "probe-608a53a4",
               "probe-9fcc9d16", "probe-b796b83f", "probe-123d9907"]

    def __init__(self):
        threading.Thread.__init__(self)
        self.load_config()

    def load_config(self):
        config = dotenv_values('.env')
        self.channel = config['CHANNEL']
        self.subscribe_key = config['SUBSCRIBE_KEY']
        self.publish_key = config['PUBLISH_KEY']

        self.kafka_server = config['KAFKA_SERVER']
        self.kafka_topic = config['KAFKA_TOPIC']

    def initialize_pubnub_connector(self):
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = self.subscribe_key
        pnconfig.publish_key = self.publish_key
        self.pubnub = PubNub(pnconfig)
        self.callback = SensorDataCallback()
        self.callback.sink = self.producer

    def subscribe_channel(self, channel_id):
        self.pubnub.add_listener(self.callback)
        self.pubnub.subscribe().channels(channel_id).execute()

    def create_producer(self):
        print("Connecting to Kafka brokers")
        for i in range(0, 6):
            try:
                producer = KafkaProducer(bootstrap_servers=[self.kafka_server],
                                value_serializer=lambda x: dumps(x).encode('utf-8'))
                print("Connected to Kafka")
                return producer
            except errors.NoBrokersAvailable:
                print("Waiting for brokers to become available")
                sleep(10)

        raise RuntimeError("Failed to connect to brokers within 60 seconds")

    def run(self):
        self.producer = self.create_producer()

        print('# Init & Subscribe to Channel: ' + self.channel)
        print()
        self.initialize_pubnub_connector()
        self.subscribe_channel(self.channel)

        count = 0
        actual_time = datetime.datetime.utcnow()
        start_time = datetime.datetime.utcnow()
        while True:
            pn_message = self.callback.message_
            if pn_message is not None:
                __message = {
                    'sensor_id': pn_message['sensor_uuid'],
                    'ambient_temperature': float(pn_message['ambient_temperature']),
                    'humidity': float(pn_message['humidity']),
                    'ingesttime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                }
                
                self.producer.send(self.kafka_topic, __message)

                count += 1
                elapsed_time = datetime.timedelta.total_seconds(actual_time - start_time)
                if elapsed_time >= 60 :
                    print(f'# Total messages in 60s: {count}')
                    print()
                    count = 0
                    start_time = datetime.datetime.utcnow()
                actual_time = datetime.datetime.utcnow()
                sleep(2)


if __name__ == '__main__':
    threads = [
        ProducerSensorData()
    ]

    for t in threads:
        t.start()
