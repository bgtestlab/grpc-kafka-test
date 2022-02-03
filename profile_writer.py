import json

import grpc
from profile_pb2 import (
    Profile,
)
import profile_pb2_grpc
from kafka import KafkaProducer

"""
Kafka configuration
"""

TOPIC_NAME = "event"
KAFKA_SERVER = "localhost:9092"


def _send_logs_to_consumer():
    producer.send(
        TOPIC_NAME,
        {"profile_writer": "Succeed on profile data creation!"},
    )
    producer.flush()


def write_profile():
    """
    Send profile creation request to Profile Service
    """

    channel = grpc.insecure_channel("localhost:50051")
    stub = profile_pb2_grpc.ProfileServiceStub(channel)

    # Update this with desired payload
    profile = Profile(
        id=4,
        name="Markus",
        team=Profile.Team.APPLE,
        role=Profile.Role.QA_MANAGER,
        channels=[Profile.Channel.OFFICE, Profile.Channel.HAVE_FUN],
    )
    response = stub.Create(profile)
    if response:
        _send_logs_to_consumer()


if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )

    producer.send(TOPIC_NAME, {"profile_writer": "Sending profile creation request..."})
    producer.flush()

    write_profile()
