import grpc

from interfaces import User_pb2_grpc, User_pb2
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter


class UserClient():

    def __init__(self, port):
        channel = grpc.insecure_channel(f"localhost:{port}")
        self.stub = User_pb2_grpc.UserServiceStub(channel)

    def create_user(self, user):
        return self.stub.CreateUser(user)

    def read_user(self, user):
        return self.stub.ReadUser(user)

    def update_user(self, user):
        return self.stub.UpdateUser(user)

    def delete_user(self, user):
        return self.stub.DeleteUser(user)

    def list_all_users(self, *args, **kargs):
        return self.stub.ListAllUsers(User_pb2.Empty())


def start(port=8000):
    completer = WordCompleter([
        "create_user",
        "read_user",
        "update_user",
        "delete_user",
        "list_all_users"
    ])
    session = PromptSession(completer=completer)
    client = UserClient(port)

    def parse(text):
        text = text.strip()
        try:
            cmd, name = text.split(' ')
        except:
            cmd, name = text, ''
        finally:
            return cmd, name

    while True:
        try:
            text = session.prompt("grpc-client >>> ")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        cmd, name = parse(text)
        message = User_pb2.User()
        message.name = name

        client_method = getattr(client, cmd)
        res = client_method(message)
        print(res)

    print("Exiting!")
