###############################################################################
# Build TCC Infrastructure
###############################################################################

FROM apache/flink:1.13.1-scala_2.12-java8
ARG FLINK_VERSION=1.13.1

# Install pyflink
RUN set -ex; \
  apt-get update; \
  apt-get -y install git-all; \
  apt-get -y install python3; \
  apt-get -y install python3-pip; \
  apt-get -y install python3-dev; \
  ln -s /usr/bin/python3 /usr/bin/python; \
  ln -s /usr/bin/pip3 /usr/bin/pip; \
  apt-get update; \
  python -m pip install --upgrade pip; \
  pip install apache-flink==1.13.1; \
  pip install kafka-python;


# Download connector libraries
RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-json/${FLINK_VERSION}/flink-json-${FLINK_VERSION}.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka_2.12/${FLINK_VERSION}/flink-sql-connector-kafka_2.12-${FLINK_VERSION}.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc_2.11/${FLINK_VERSION}/flink-connector-jdbc_2.11-${FLINK_VERSION}.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/mysql/mysql-connector-java/8.0.25/mysql-connector-java-8.0.25.jar;


RUN echo "taskmanager.memory.jvm-metaspace.size: 512m" >> /opt/flink/conf/flink-conf.yaml;

WORKDIR /opt/flink
