from concurrent import futures
import logging

import grpc

import users_pb2_grpc as users_service
import user_types_pb2 as users_messages


class UsersService(users_service.UsersServicer):
    users = []

    def CreateUser(self, request, context):
        metadata = dict(context.invocation_metadata())
        print(metadata)
        user = users_messages.User(username=request.username, user_id=request.user_id)
        if user not in self.users:
            self.users.append(user)
        return users_messages.CreateUserResult(user=user)

    def GetUsers(self, request, context):
        for user in request.user:
            user = users_messages.User(username=user.username, user_id=user.user_id)
            if user in self.users:
                yield users_messages.GetUsersResult(user=user)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_service.add_UsersServicer_to_server(UsersService(), server)
    server.add_insecure_port('[::]:50051')
    print("server is starting...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
