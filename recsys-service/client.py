import grpc
import recsys_pb2
import recsys_pb2_grpc


def run():
    # Open a gRPC channel
    channel = grpc.insecure_channel("localhost:10001")

    # Create a stub (client)
    stub = recsys_pb2_grpc.RecSysEngineStub(channel)

    # Create a valid request message
    communities_request = recsys_pb2.CommunitiesRequest(
        ids=[62258607, 221105865, 199008704]
    )

    # Make the call
    response = stub.Communities(communities_request)

    # Print response
    print(response)


if __name__ == "__main__":
    run()
