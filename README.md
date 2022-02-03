# grpc_kafka_test
## Preconditions
Run Kafka Zookeeper and Broker services on the Kafka folder
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

## Generate grpc files
```bash
python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ profile.proto
python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ history.proto
```

## Steps
Run kafka consumer first
```bash
python kafka_consumer.py
```

Next, open two additional terminals run services each
```bash
python profile_service.py
python history_service.py
```

Then, run test files
```bash
python profile_reader.py
python profile_writer.py
python profile_reader.py
```
