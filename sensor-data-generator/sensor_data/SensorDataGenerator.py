

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

class SensorDataGenerator():
    def __init__(self, channel, sink):
        self._pnconfig = PNConfiguration()
        self._pubnub = None
        self._channel = channel
        self._sink = sink
        self._started = False
        self._stop = False

    def initialize(self):
        self._pnconfig.publish_key = "myPublishKey"
        self._pnconfig.subscribe_key = "mySubscribeKey"
        self._pnconfig.uuid = "serverUUID-SUB"

        self._pubnub = PubNub(self._pnconfig)
        self._pubnub.add_listener(SensorDataReaderCallback(self._sink))

    def start(self):
        self._pubnub.subscribe().channels(self._channel).with_presence().execute()

    def stop(self):
        pass

class SensorDataSink():
    def write(self):
        pass

class SensorDataReaderCallback(SubscribeCallback):
    def __init__(self, sink):
        super().__init__(self)
        self._sink = sink

    def message(self, pubnub, event):
        print("[MESSAGE received]")

        if event.message["update"] == "42":
            print("The publisher has ended the session.")
            exit(0)
        else:
            print("{}".format(event.message))
            self._sink.write(event.message)

    def presence(self, pubnub, event):
        print("[PRESENCE: {}]".format(event.event))
        print("uuid: {}, channel: {}".format(event.uuid, event.channel))
        print()

    def status(self, pubnub, event):
        if event.category == PNStatusCategory.PNConnectedCategory:
            print("[STATUS: PNConnectedCategory]")
            print("connected to channels: {}".format(event.affected_channels))
            print()
