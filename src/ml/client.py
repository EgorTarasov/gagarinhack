import grpc
from .stubs import search_pb2, search_pb2_grpc


def run():
    channel = grpc.insecure_channel("45.124.43.156:10000")

    stub = search_pb2_grpc.SearchEngineStub(channel)

    request = search_pb2.Query("some text", "some model")

    response = stub.Respond(request)
    print("single response", response)

    print("stream response:\n")

    for i in stub.RespondStream(request):
        print(i)


if __name__ == "__main__":
    run()
