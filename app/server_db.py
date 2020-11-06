from interfaces import User_pb2


class FakeDB():
    users = User_pb2.Users()
    names = dict()

    def CreateUser(self, user):
        if user.name and (user.name not in self.names.keys()):
            self.users.items.append(user)
            self.names[user.name] = len(self.users.items)
            return user
        return User_pb2.User()

    def ReadUser(self, user):
        if idx := self.names.get(user.name):
            return self.users.items[idx-1]
        return User_pb2.User()

    def UpdateUser(self, user):
        if idx := self.names.get(user.name):
            return self.users.items[idx-1]
        return User_pb2.User()

    def DeleteUser(self, user):
        if idx := self.names.get(user.name):
            self.names.pop(user.name)
            return self.users.items.pop(idx-1)
        return User_pb2.User()

    def ListAllUsers(self):
        return self.users
