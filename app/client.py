import grpc

from interfaces import User_pb2_grpc, User_pb2
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter


def start(port=8000):
    completer = WordCompleter([
        "create_user",
        "read_user",
        "update_user",
        "delete_user",
        "list_all_users"
    ])
    session = PromptSession(completer=completer)
    channel = grpc.insecure_channel(f"localhost:{port}")
    stub = User_pb2_grpc.UserServiceStub(channel)

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

        if cmd == "create_user" and name:
            response = stub.CreateUser(message)
            print(response)

        if cmd == "read_user" and name:
            response = stub.ReadUser(message)
            print(response)

        if cmd == "update_user" and name:
            response = stub.UpdateUser(message)
            print(response)

        if cmd == "delete_user" and name:
            response = stub.DeleteUser(message)
            print(response)

        if cmd == "list_all_users":
            message = User_pb2.Empty()
            response = stub.ListAllUsers(message)
            for user in response.items:
                print(user)

    print("Exiting!")
