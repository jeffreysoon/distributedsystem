from __future__ import print_function

import logging

import grpc
import user_types_pb2 as users_messages
import users_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    metadata = [('ip', '127.0.0.1')]
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        response = stub.CreateUser(users_messages.CreateUserRequest(username='tester', user_id=123), metadata=metadata)
        print(response.user)
        response = stub.CreateUser(users_messages.CreateUserRequest(username='tester2', user_id=456), metadata=metadata)
        print(response.user)
        request = users_messages.GetUsersRequest(user=[users_messages.User(username='tester', user_id=123), users_messages.User(username='tester3', user_id=456)])
        response = stub.GetUsers(request)
        for resp in response:
            print(resp)


if __name__ == '__main__':
    logging.basicConfig()
    run()
