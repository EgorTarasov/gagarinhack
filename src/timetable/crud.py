import os

from asyncpg.pool import PoolConnectionProxy
from .models import Lesson
import pandas as pd


async def save_schedule(db_conn: PoolConnectionProxy, schedule: pd.DataFrame):
    tmp_file = "tmp/tmp.csv"
    schedule.to_csv(tmp_file, sep=",")
    await db_conn.copy_to_table('lessons')
    os.remove(tmp_file)
