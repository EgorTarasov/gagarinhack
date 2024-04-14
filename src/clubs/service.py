from asyncpg.pool import PoolConnectionProxy

from auth import service
from recsys.client import recsys_client


async def get_recommended_clubs(db_conn: PoolConnectionProxy, user_id: int):
    group_ids = await service.get_vk_groups_ids(db_conn, user_id)
    return recsys_client.get_communities(group_ids)

