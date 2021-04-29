from dotenv import dotenv_values

from sensor_data.SensorDataSink import SensorDataSink
from sensor_data.SensorDataGenerator import SensorDataGenerator

sink = SensorDataSink(console=True)
sensor = SensorDataGenerator(sink)

if __name__ == '__main__':
    sensor.start()
