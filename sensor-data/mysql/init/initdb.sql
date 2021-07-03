DROP DATABASE IF EXISTS sensors_db;
CREATE DATABASE sensors_db;

use sensors_db;

CREATE TABLE sensor_data (sensor_id VARCHAR(20), ambient_temperature DOUBLE, humidity DOUBLE, PRIMARY KEY (sensor_id));