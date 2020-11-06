from interfaces import User_pb2, User_pb2_grpc
import grpc
from concurrent.futures import ThreadPoolExecutor
import time


class UserServer(User_pb2_grpc.UserServiceServicer):
    users = User_pb2.Users()
    names = dict()

    def CreateUser(self, request, context):
        if request.name not in self.names.keys():
            self.users.items.append(request)
            self.names[request.name] = len(self.users.items)
        return request

    def ReadUser(self, request, context):
        if idx := self.names.get(request.name):
            return self.users.items[idx-1]
        return User_pb2.User()

    def UpdateUser(self, request, context):
        if idx := self.names.get(request.name):
            return self.users.items[idx-1]
        return User_pb2.User()

    def DeleteUser(self, request, context):
        if idx := self.names.get(request.name):
            self.names.pop(request.name)
            return self.users.items.pop(idx-1)
        return User_pb2.User()

    def ListAllUsers(self, request, context):
        return self.users


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
