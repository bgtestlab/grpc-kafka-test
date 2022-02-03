import copy
from concurrent import futures
from typing import List

import grpc

import history_pb2_grpc
from history_pb2 import HistoryRequest
from profile_pb2 import (
    Profile,
    CreateResponse,
    ListProfiles,
)

import profile_pb2_grpc


"""
Profile
"""
profile_list = [
    Profile(
        id=1,
        name="Shane",
        team=Profile.Team.APPLE,
        role=Profile.Role.PRODUCT_OWNER,
        channels=[Profile.Channel.OFFICE, Profile.Channel.TODAY_I_LEARNED],
    ),
    Profile(
        id=2,
        name="Kian",
        team=Profile.Team.DURIAN,
        role=Profile.Role.ENGINEER,
        channels=[Profile.Channel.OFFICE, Profile.Channel.DEVELOPMENT],
    ),
    Profile(
        id=3,
        name="Nicky",
        team=Profile.Team.BANANA,
        role=Profile.Role.DESIGNER,
        channels=[
            Profile.Channel.OFFICE,
            Profile.Channel.HAVE_FUN,
            Profile.Channel.TODAY_I_LEARNED,
        ],
    ),
]


class ProfileServicer(profile_pb2_grpc.ProfileServiceServicer):
    def Get(self, request, context):
        name = request.name
        print(f"Received a profile request with name: {name}")
        founds = [profile for profile in profile_list if profile.name == name]

        if not len(founds):
            context.abort(grpc.StatusCode.NOT_FOUND, "Name not found")

        # Add previous teams
        profiles = copy.deepcopy(founds)
        for profile in profiles:
            profile.previousTeams.extend(self._history_request(profile.id))

        return ListProfiles(profiles=profiles)

    def GetList(self, request, context):
        # Add previous teams
        profiles = copy.deepcopy(profile_list)
        for profile in profiles:
            profile.previousTeams.extend(self._history_request(profile.id))

        return ListProfiles(profiles=profiles)

    def Create(self, request, context):
        print(f"Received a profile request with name: {request.name}")

        profile_list.append(
            Profile(
                id=request.id,
                name=request.name,
                team=request.team,
                role=request.role,
                channels=request.channels,
            )
        )

        print(f"Profile added: {profile_list[-1]}")

        return CreateResponse(status=True)

    def _history_request(self, id) -> List:
        """
        Get messages from History Service
        """

        channel = grpc.insecure_channel("localhost:50052")
        stub = history_pb2_grpc.HistoryServiceStub(channel)

        # Request history with an ID
        print(f"Request a specific history with an ID: {id}")
        response = stub.Get(HistoryRequest(id=id))
        print(f"Found previous teams: {response}")

        return response.teams


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    profile_pb2_grpc.add_ProfileServiceServicer_to_server(ProfileServicer(), server)
    print("Server starting on port 50051...")
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination(180)


if __name__ == "__main__":
    serve()
