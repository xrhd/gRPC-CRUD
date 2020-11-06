from interfaces import User_pb2, User_pb2_grpc
import grpc
from concurrent.futures import ThreadPoolExecutor
import time
from .server_db import FakeDB


class UserServer(User_pb2_grpc.UserServiceServicer):
    db = FakeDB()

    def CreateUser(self, request, context):
        return self.db.CreateUser(request)

    def ReadUser(self, request, context):
        return self.db.ReadUser(request)

    def UpdateUser(self, request, context):
        return self.db.UpdateUser(request)

    def DeleteUser(self, request, context):
        return self.db.DeleteUser(request)

    def ListAllUsers(self, request, context):
        return self.db.ListAllUsers()


def serve(port=8000):
    server = grpc.server(ThreadPoolExecutor(max_workers=5))
    User_pb2_grpc.add_UserServiceServicer_to_server(UserServer(), server)

    print(f"Starting server at port: {port}")
    server.add_insecure_port(f"[::]:{port}")
    server.start()

    # Since server is running in threads, it doesn't block flow so the program just ends.
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(1)
