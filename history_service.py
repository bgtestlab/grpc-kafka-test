from concurrent import futures

import grpc
from history_pb2 import (
    History,
    HistoryResponse,
)
import history_pb2_grpc
from profile_pb2 import Profile


history_list = [
    History(
        id=1,
        name="Shane",
        teams=[Profile.Team.DURIAN, Profile.Team.CHERRY],
    ),
    History(
        id=2,
        name="Kian",
        teams=[],
    ),
    History(
        id=3,
        name="Nicky",
        teams=[Profile.Team.CHERRY],
    ),
    History(
        id=4,
        name="Markus",
        teams=[Profile.Team.APPLE],
    ),
]


class HistoryServicer(history_pb2_grpc.HistoryServiceServicer):
    def Get(self, request, context):
        id = request.id
        print(f"Received a history request with id: {id}")
        for history in history_list:
            if history.id == id:
                return HistoryResponse(teams=history.teams)

        context.abort(grpc.StatusCode.NOT_FOUND, "ID not found")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    history_pb2_grpc.add_HistoryServiceServicer_to_server(HistoryServicer(), server)
    print("Server starting on port 50052...")
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination(180)


if __name__ == "__main__":
    serve()
