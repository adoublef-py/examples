from concurrent import futures

import grpc
from protobuf.greet_pb2 import ServerOutput
from protobuf.greet_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server


class Greeter(GreeterServicer):
   def greet(self, request, context):
      print("Got request " + str(request))
      return ServerOutput(message='{0} {1}!'.format(request.greeting, request.name))


def server():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
   add_GreeterServicer_to_server(Greeter(), server)
   server.add_insecure_port('[::]:50051')
   print("gRPC starting")
   server.start()
   server.wait_for_termination()


server()
