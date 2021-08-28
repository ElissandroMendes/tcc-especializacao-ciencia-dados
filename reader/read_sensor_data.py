from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, DataTypes, EnvironmentSettings

def read_sensor_data():
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(stream_execution_environment=env)
    t_env.get_config().get_configuration().set_boolean("python.fn-execution.memory.managed", True)

    create_kafka_source_ddl = """
            CREATE TABLE sensor_data_in(
                sensor_id VARCHAR,
                ambient_temperature DOUBLE,
                humidity DOUBLE,
                ingesttime TIMESTAMP(3)
            ) WITH (
              'connector.type' = 'kafka',
              'connector.version' = 'universal',
              'connector.topic' = 'sensor-data',
              'connector.properties.bootstrap.servers' = 'kafka:29092',
              'connector.startup-mode' = 'latest-offset',
              'format.type' = 'json'
            )
            """
    # data_sensor_table_sink = """
    #     CREATE TABLE sensor_data_out (
    #         sensor_id VARCHAR(20),
    #         ambient_temperature DOUBLE,
    #         humidity DOUBLE,
    #         ingesttime TIMESTAMP(6),
    #         PRIMARY KEY (sensor_id) NOT ENFORCED
    #     ) WITH (
    #         'connector' = 'jdbc',
    #         'url' = 'jdbc:mysql://db:3306/sensors_db',
    #         'table-name' = 'sensor_data',
    #         'username' = 'root',
    #         'password' = 'tcc-infra'
    #     )    
    # """
    data_sensor_table_sink = """
        CREATE TABLE sensor_data_out (
            sensor_id VARCHAR(20),
            ambient_temperature DOUBLE,
            humidity DOUBLE,
            ingesttime TIMESTAMP(3),
            PRIMARY KEY (sensor_id) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:mysql://db:3306/sensors_db',
            'table-name' = 'sensor_data',
            'username' = 'root',
            'password' = 'tcc-infra'
        )    
    """
    create_es_sink_ddl = """
        CREATE TABLE sensor_data_out (
            sensor_id VARCHAR,
            total_ambient_temperature DOUBLE
        ) WITH (
            'connector' = 'print',
            'print-identifier' = 'sensor-data '
        )
        """

    t_env.execute_sql(create_kafka_source_ddl)
    t_env.execute_sql(data_sensor_table_sink)

    # .select("sensor_id, ambient_temperature") \
    # .group_by("sensor_id") \
    # .select("sensor_id, sum(ambient_temperature) as ambient_temperature") \
    t_env.from_path("sensor_data_in") \
        .execute_insert("sensor_data_out")

if __name__ == '__main__':
    read_sensor_data()

