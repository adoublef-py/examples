# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protobuf import greet_pb2 as protobuf_dot_greet__pb2


class GreeterStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.greet = channel.unary_unary(
                '/Greeter/greet',
                request_serializer=protobuf_dot_greet__pb2.ClientInput.SerializeToString,
                response_deserializer=protobuf_dot_greet__pb2.ServerOutput.FromString,
                )


class GreeterServicer(object):
    """Missing associated documentation comment in .proto file."""

    def greet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GreeterServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'greet': grpc.unary_unary_rpc_method_handler(
                    servicer.greet,
                    request_deserializer=protobuf_dot_greet__pb2.ClientInput.FromString,
                    response_serializer=protobuf_dot_greet__pb2.ServerOutput.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Greeter', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Greeter(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def greet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Greeter/greet',
            protobuf_dot_greet__pb2.ClientInput.SerializeToString,
            protobuf_dot_greet__pb2.ServerOutput.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
