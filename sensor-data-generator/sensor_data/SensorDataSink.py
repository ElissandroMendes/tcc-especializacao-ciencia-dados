import json
import pprint

from dotenv import dotenv_values
from kafka import KafkaProducer

class SensorDataSink():
    def __init__(self, console=True):
        self._to_console = console
        self._config = dotenv_values("../.env")
        pprint(self._config)
        self.producer = KafkaProducer(bootstrap_servers=self._config.get("KAFKA_SERVER"),
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def write(self, message):
        if self._to_console:
            print(f"Message: {message}")
        else:
            self.producer.send(self._config.KAFKA_TOPIC, message)
