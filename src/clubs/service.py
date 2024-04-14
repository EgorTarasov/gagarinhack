from asyncpg.pool import PoolConnectionProxy
from . import crud
from auth import service
from recsys.client import recsys_client
from utils.logging import log


async def get_recommended_clubs(db_conn: PoolConnectionProxy, user_id: int):
    group_ids = await crud.select_user_groups(db_conn, user_id)
    log.debug(group_ids)
    res = recsys_client.get_communities(group_ids)
    return res
