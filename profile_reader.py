import json

import grpc

from profile_pb2 import (
    Empty,
    ProfileRequest,
    Profile,
)
import profile_pb2_grpc
from kafka import KafkaProducer


"""
Kafka configuration
"""

TOPIC_NAME = "event"
KAFKA_SERVER = "localhost:9092"


def _send_logs_to_producer(response):
    profiles = {}
    for profile in response:
        profiles[str(profile.id)] = {
            "name": profile.name,
            "team": profile.Team.Name(profile.team),
            "role": profile.Role.Name(profile.role),
        }

        # Add channels
        list = []
        for channel in profile.channels:
            list.append(Profile.Channel.Name(channel))
        profiles["channels"] = list

        # Add previousTeams
        list.clear()
        for team in profile.previousTeams:
            list.append(Profile.Team.Name(team))
        profiles["previousTeams"] = list

    producer.send(TOPIC_NAME, profiles)
    producer.flush()


def read_profile():
    """Send profile data request to Profile Service"""

    channel = grpc.insecure_channel("localhost:50051")
    stub = profile_pb2_grpc.ProfileServiceStub(channel)

    # Request profile with a name
    producer.send(TOPIC_NAME, {"profile_reader": "Request profile with a name..."})
    producer.flush()
    response = stub.Get(ProfileRequest(name="Shane")).profiles

    # Send logs
    if response:
        _send_logs_to_producer(response)

    # Get all the list
    producer.send(TOPIC_NAME, {"profile_reader": "Get all the list..."})
    producer.flush()
    response = stub.GetList(Empty()).profiles

    # Send logs
    if response:
        _send_logs_to_producer(response)


if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )

    producer.send(TOPIC_NAME, {"profile_reader": "Sending profile data request..."})
    producer.flush()

    read_profile()
