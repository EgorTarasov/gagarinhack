import grpc
import recsys_pb2
import recsys_pb2_grpc
from config import cfg


class RecSysClient:
    def __init__(self, grpc_endpoint: str):
        channel = grpc.insecure_channel(grpc_endpoint)
        self.stub = recsys_pb2_grpc.RecSysEngineStub(channel)

    def __build_request(self, ids: list[int]):
        return recsys_pb2.CommunitiesRequest(
            ids=ids,
        )

    def get_communities(self, ids: list[int]):
        request = self.__build_request(ids)
        return self.stub.Communities(request)


recsys_client = RecSysClient(cfg.recsys_engine_uri)
