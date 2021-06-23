import sys

from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, CsvTableSink, DataTypes, EnvironmentSettings
from pyflink.table.descriptors import Schema, Rowtime, Json, Kafka
from pyflink.table.window import Tumble

# class Adder(GroupReduceFunction):
#     def reduce(self, iterator, collector):
#         count, word = iterator.next()
#         count += sum([x[0] for x in iterator])
#         collector.collect((count, word))

def register_source(st_env):
    json_row_def = [
        DataTypes.FIELD("sensor-id", DataTypes.STRING()),
        DataTypes.FIELD("ambient_temperature", DataTypes.DOUBLE()),
        DataTypes.FIELD("humidity", DataTypes.DOUBLE()),
        DataTypes.FIELD("timestamp", DataTypes.TIMESTAMP())
    ]
    schema_defs = Schema()\
        .field("sensor-id", DataTypes.STRING())
        .field("ambient_temperature", DataTypes.STRING())
        .field("humidity", DataTypes.STRING())
        .field("rowtime", DataTypes.TIMESTAMP())
        .rowtime(Rowtime().timestamps_from_field("timestamp").watermarks_periodic_bounded())
    st_env.connect(Kafka()
                   .version("universal")
                   .topic("sensor-data")
                   .start_from_latest()
                   .property("zookeeper.connect", "localhost:2181")
                   .property("bootstrap.servers", "localhost:19092"))\
    .with_format(Json()
        .fail_on_missing_field(True)
        .schema(DataTypes.ROW(json_row_def))
    )
    .with_schema(Schema()
                 field().)

if __name__ == '__main__':
    base_path = sys.argv[0]

    output_file = f'file://{base_path}/word_count/out.txt'

    env_settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
    # table_env = TableEnvironment.create(environment_settings=env_settings)

    s_env = StreamExecutionEnvironment.get_execution_environment()
    s_env.set_parallelism(1)
    s_env.set_stream_time_characteristic(TimeCharacteristic.EventTime)

    st_env = StreamTableEnvironment.create(s_env, environment_settings=env_settings)
    data = st_env\
        .from_elements([(1, 'Hi'), (2, 'Hello')],
                       DataTypes.ROW([DataTypes.FIELD("id", DataTypes.TINYINT()),
                                      DataTypes.FIELD("data", DataTypes.STRING())]))
    df = data.to_pandas()

    print(df)

    table_env.execute_sql("""
        CREATE TABLE random_source (
            id BIGINT, 
            data TINYINT
        ) WITH (
            'connector'='datagen',
            'fields.id.kind'='sequence',
            'fields.id.start'='1',
            'fields.id.end'='3',
            'fields.data.kind'='sequence',
            'fields.data.start'='4',
            'fields.data.end'= '6'
        )
    """)
    table = table_env.from_path("random_source")
    df1 = table.to_pandas()
    print()
    print(df1)
    # data\
    #     .flat_map(lambda x, c: [(1, word) for word in x.lower().split()])\
    #     .group_by(1)\
    #     .reduce_group(Adder(), combinable=True)\
    #     .map(lambda x: f'Count {y[0]} Word: {Y[1]}')\
    #     .write_text(output_file, write_mode=WriteMode.OVERWRITE)

    # env.execute(local=True)
