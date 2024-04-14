import grpc
from . import recsys_pb2, recsys_pb2_grpc
from config import cfg


class RecSysClient:
    def __init__(self, grpc_endpoint: str):
        self.channel = grpc.aio.insecure_channel(grpc_endpoint)
        self.stub = recsys_pb2_grpc.RecSysEngineStub(self.channel)

    def __build_request(self, ids: list[int]):
        return recsys_pb2.CommunitiesRequest(
            ids=ids,
        )

    async def get_communities(self, ids: list[int]):
        request = self.__build_request(ids)
        return await self.stub.Communities(request)


aiorecsys_client = RecSysClient(cfg.recsys_engine_uri)
