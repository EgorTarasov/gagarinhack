import grpc
from . import search_engine_pb2
from . import search_engine_pb2_grpc
from config import cfg
from typing import AsyncGenerator, NamedTuple


class MLClient:
    def __init__(self, grpc_endpoint: str):
        channel = grpc.insecure_channel(grpc_endpoint)
        self.stub = search_engine_pb2_grpc.SearchEngineStub(channel)

    def __build_request(self, query: str):
        return search_engine_pb2.Query(
            body=query,
            model="test model",
        )

    def single_response(self, query: str):
        request = self.__build_request(query)
        return self.stub.Respond(request)

    def stream_response(self, query: str):
        request = self.__build_request(query)
        for response in self.stub.RespondStream(request):
            yield response.body


ml_client = MLClient(cfg.search_engine_uri)


async def get_ml_service() -> AsyncGenerator[MLClient, None]:
    yield ml_client
