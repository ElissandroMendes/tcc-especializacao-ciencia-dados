DROP DATABASE IF EXISTS sensors_db;
CREATE DATABASE sensors_db;

GRANT ALL ON sensors_db.* to 'root'@'172.%' IDENTIFIED BY 'tcc-infra';

use sensors_db;
CREATE TABLE sensor_data (sensor_id VARCHAR(20), ambient_temperature DOUBLE, humidity DOUBLE, ingesttime TIMESTAMP(3), PRIMARY KEY (sensor_id));
