import time
import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from kafka import KafkaConsumer, KafkaProducer

stream = None


def create_and_subscribe_consumer():
    global stream
    print("Creating Consumer instance")
    stream = KafkaConsumer(bootstrap_servers='localhost:9092',
                           auto_offset_reset='latest',
                           value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    # print("Subscribe to Topic")
    # stream.subscribe(['sensor-data'])


def load_data():
    data = [
        {'sensor_uuid': 'probe-b796b83f', 'ambient_temperature': 28.47, 'humidity': 78.5523,
         'radiation_level': 202, 'photosensor': 793.32, 'timestamp': 1615680200},
        {'sensor_uuid': 'probe-b796b83f', 'ambient_temperature': 19.16, 'humidity': 82.5701,
         'radiation_level': 199, 'photosensor': 817.43, 'timestamp': 1615680197},
        {'sensor_uuid': 'probe-28500df7', 'ambient_temperature': 17.91, 'humidity': 76.0004,
         'radiation_level': 200, 'photosensor': 847.72, 'timestamp': 1615680191},
        {'sensor_uuid': 'probe-28500df7', 'ambient_temperature': 21.33, 'humidity': 86.3682,
         'radiation_level': 194, 'photosensor': 805.9, 'timestamp': 1615680194}
    ]
    return data


def get_data():
    d = np.random.randn(10, 2)
    data = pd.DataFrame(d, columns=["sensor0", "sensor1"])
    print("Pooling message")
    # for message in stream:
    #     print(f'From [ {message.topic} ] -> {message.value}')
    return data


def plot_data():
    global chart
    hist_data = get_data()
    chart.line_chart(hist_data, use_container_width=True)
    while True:
        hist_data = get_data()
        chart.line_chart(hist_data, use_container_width=True)
        time.sleep(.1)


def plot_data_1():
    global chart
    while True:
        hist_data = get_data()
        data_0 = go.Scatter(x=hist_data.index, y=hist_data["sensor0"])
        data_1 = go.Scatter(x=hist_data.index, y=hist_data["sensor1"])
        chart.plotly_chart(
            [data_0, data_1], filename='extend plot', fileopt='extend')
        time.sleep(.1)


st.title("Dashboard Grid's Sensors")
chart = st.empty()
create_and_subscribe_consumer()
plot_data_1()
