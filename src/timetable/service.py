# TODO: Parse timetable from url
import requests
from config import cfg
from utils.logging import log
import bs4
import pandas as pd
import numpy as np
from . import crud
from asyncpg.pool import PoolConnectionProxy
import asyncio


def data_preprocess(df: pd.DataFrame, group, odd_even: str):
    cur = df.loc[:, [group, "order", "weekday", f"{group}-кабинеты", "lesson_time"]]
    cur.dropna(inplace=True)
    cur.rename(columns={f"{group}-кабинеты": "room_id", group: "title",
                        }, inplace=True, )

    cur["teacher_fio"] = cur["title"].str.split("\n").str[1]
    cur["type"] = cur["title"].str.extract(r"\(([^)]*)\)[^(]*$")
    cur["title"] = (cur["title"].str.split("\n").str[0].str.replace("(Лекционные)", " ").str.replace("(Лабораторные)",
                                                                                                     " ").str.replace(
            "(Практические)", " ").str.replace(r"с \d\d:\d\d до \d\d:\d\d ", "", regex=True).str.split("п.г. "))
    cur["title"] = cur["title"].map(lambda x: x[0] if len(x) == 1 else x[1])
    cur["title"] = cur["title"].str.strip()

    cur["odd_even_week"] = 0 if odd_even == "even" else 1
    cur["group_name"] = group

    return cur


async def upload_schedules(db_conn: PoolConnectionProxy):
    # FIXME: не обновлять расписание если найденные файлы имеют название уже загруженных
    log.debug("Uploading schedules")
    response = requests.get(cfg.lms_base_url + cfg.lms_timetable_path, timeout=59)
    if response.status_code != 200:
        raise Exception("Can't get schedule")
    log.debug("Got schedule")
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    div = soup.find("div", class_="data")
    links = [cfg.lms_base_url + link["href"] for link in div.find_all("a") if "ibo" not in link["href"]]

    schedules = pd.DataFrame()
    for link in links:
        data = pd.ExcelFile(link)
        log.debug(link)

        for sheet_name in data.sheet_names:
            if "курс" not in sheet_name:
                continue

            df = pd.read_excel(data, sheet_name=sheet_name)

            weekdays = df.iloc[:, 0].fillna(method="ffill")
            df["Дата"] = weekdays
            lesson_orders = df.iloc[:, 1].fillna(method="ffill")
            df["Номер"] = lesson_orders
            df["Номер"] = df["Номер"].astype(int, errors="ignore")

            columns = list(pd.DataFrame(df.columns).replace(r"^Unnamed.*", np.nan, regex=True).ffill(limit=1)[0])
            df.columns = columns

            groups = set(columns)
            try:
                groups.remove("Номер")
                groups.remove("Дата")
                groups.remove("Время")
                groups.remove(np.nan)
            except KeyError:
                pass

            df.columns = [f"{col}-кабинеты" if is_duplicated else col for col, is_duplicated in
                          zip(df.columns, df.columns.duplicated(keep="first"))]
            df = df.loc[:, ~df.columns.str.startswith("nan", na=False)]

            df = df.rename(columns={"Дата": "weekday", "Номер": "arrangement",
                                    })
            df["weekday"] = df["weekday"].map(
                    {"Понедельник": 0, "Вторник": 1, "Среда": 2, "Четверг": 3, "Пятница": 4, "Суббота": 5,
                     "Воскресенье": 6,
                     })
            df["weekday"] = df["weekday"].astype(int, errors="ignore")
            df["lesson_time"] = df.iloc[:, 2].fillna(method="ffill")

            odd = df.iloc[::2, :]
            even = df.iloc[1::2, :]

            for group in groups:
                cur_odd = data_preprocess(odd, group, "odd")
                cur_even = data_preprocess(even, group, "even")
                cur = pd.concat([cur_even, cur_odd])
                schedules = pd.concat([schedules, cur])

    schedules.index = range(len(schedules))
    await asyncio.create_task(crud.save_schedule(db_conn, schedules))

