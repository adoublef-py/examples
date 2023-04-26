import grpc

from protobuf.greet_pb2 import ClientInput
from protobuf.greet_pb2_grpc import GreeterStub


def run():
   with grpc.insecure_channel('localhost:50051') as channel:
      stub = GreeterStub(channel)
      response = stub.greet(ClientInput(name='John', greeting="Yo"))
   print("Greeter client received following from server: " + response.message)


run()
