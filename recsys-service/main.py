"""
recsys = Recsys(
    model_name="Tochka-AI/ruRoPEBert-e5-base-2k",
    db_params=db_params,
    ch_params=ch_params,
)
vk_group_ids = [159224823, 186113198]
recsys.main(vk_group_ids)
# output -> [('Баскетбол', 0.43349232486670697), ('Музыкальный клуб', 0.4149073748957852)]

"""

import json
from concurrent import futures
import logging
from recsys import Recsys
from recsys_pb2 import CommunitiesRequest, CommunitiesResponse, Community
from recsys_pb2_grpc import (
    RecSysEngine,
    RecSysEngineStub,
    add_RecSysEngineServicer_to_server,
)
from grpc import ServicerContext, server


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class RecSysServicer(RecSysEngine):
    def __init__(self, recsys: Recsys) -> None:
        self.recsys = recsys
        super().__init__()

    def Communities(self, request: CommunitiesRequest, ctx) -> CommunitiesResponse:
        log.debug(f"request = {request}")
        log.debug(f"ctx = {ctx}")
        print(type(request.ids))
        group_ids = [i for i in request.ids]
        communities = self.recsys.main(group_ids)
        response = CommunitiesResponse(
            communities=[
                Community(name=str(title), score=float(similarity))
                for title, similarity in communities
            ]
        )
        return response


def serve():
    # FIXME: use environment variables
    with open("db.json", "r") as f:
        db_params = json.load(f)

    with open("ch.json", "r") as f:
        ch_params = json.load(f)

    s = server(futures.ThreadPoolExecutor(max_workers=10))
    recsys = Recsys(
        model_name="Tochka-AI/ruRoPEBert-e5-base-2k",
        db_params=db_params,
        ch_params=ch_params,
    )
    recsys_servicer = RecSysServicer(recsys)
    add_RecSysEngineServicer_to_server(recsys_servicer, s)
    s.add_insecure_port("[::]:10001")
    s.start()
    log.info("Server started")
    s.wait_for_termination()


if __name__ == "__main__":
    serve()
