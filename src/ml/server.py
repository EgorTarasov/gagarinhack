from concurrent import futures
from grpc import server
from stubs import search_pb2, search_pb2_grpc, Query, Response


class SearchEngine(search_pb2_grpc.SearchEngineServicer):
    def __init__(self, model) -> None:
        super().__init__()
        self.model = model

    def Respond(self, request, context):
        # модель тут

        return Response("single response", "none")

    def RespondStream(self, request, context):
        for i in range(20):
            yield Response(f"msg{i}", context="some context")


def serve():
    s = server(futures.ThreadPoolExecutor(max_workers=10))

    search_pb2_grpc.add_SearchEngineServicer_to_server(SearchEngine, s)
    s.add_insecure_port("[::]:10000")
    s.start()
    s.wait_for_termination()


if __name__ == "__main__":
    serve()
