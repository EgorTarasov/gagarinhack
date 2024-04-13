import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)

from config import cfg
from enum import Enum


dp = Dispatcher()
bot = Bot(cfg.telegram_token)


def get_link(token: str) -> str:
    return f"https://t.me/{cfg.telegram_bot_name}?start={token}"


# def send_notification(user_id: int, message: str):
#     bot.send_message(user_id, message)


class FeedbackRequest(Enum):
    first = "first"
    week = "week"
    month = "month"


class Messages:
    @staticmethod
    def feedback_first_day(fullname: str):
        return f"""Добрый день, {fullname},
🌟 Первый день – это всегда волнительно! Как ощущения? Нужна ли тебе помощь или есть организационные вопросы?

Жду твоих впечатлений и готов помочь с чем угодно!
"""

    @staticmethod
    def feedback_first_week(fullname: str):
        return f"""
Здравствуйте, {fullname},

🚀 Уже неделя обучения за плечами! Как твои впечатления? Может, есть идеи или предложения, которыми хочешь поделиться?

Твоё мнение очень важно для нас. Давай работать вместе на улучшение процессов!

"""

    @staticmethod
    def feedback_first_month(fullname: str):
        return f"""
Приветствуем вас, {fullname},

🌟 Первый месяц в новом месте – это большое достижение! Какие моменты были особенно запоминающимися? Что бы ты хотел(а) изменить или улучшить?

Твои отзывы помогают нам расти и развиваться. Жду твоих идей и предложений!


С уважением,
Алина, твой умный помощник.
"""


class FeedbackCallbackData(CallbackData, prefix="adm"):
    type: FeedbackRequest
    user_id: int


async def request_feedback(user_id: int, fullname: str, feedback: FeedbackRequest):
    message = ""
    match feedback:
        case FeedbackRequest.first:
            message = Messages.feedback_first_day(fullname)
        case FeedbackRequest.week:
            message = Messages.feedback_first_week(fullname)
        case FeedbackRequest.month:
            message = Messages.feedback_first_month(fullname)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Пройти опрос",
                    callback_data=FeedbackCallbackData(
                        type=feedback, user_id=user_id
                    ).pack(),
                )
            ]
        ]
    )
    await bot.send_message(
        user_id,
        message,
        reply_markup=keyboard,
    )


@dp.message(CommandStart())
async def command_start_handler(message: Message, command: CommandStart) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f"Привет студенту ITHub!"
        f"Наш бот Алина поможет вам найти клубы единомышленников, "
        f"а также соберёт от вас обратную связь по процессу адаптации в колледже, которая поможет нам стать лучше."
    )


class Survey(StatesGroup):
    rating = State()
    feeling = State()
    info = State()


class SurveyResult(CallbackData, prefix="survey_"):
    rating: int = 0
    feeling: int = 0
    info: str = ""


rating_options_sentence = {
    "Сервис запутанный и неэффективный.": 1,
    "Были некоторые полезные моменты, но в целом сервис требует улучшений.": 2,
    "Сервис организован неплохо, но есть пространство для улучшений.": 3,
    "Сервис понятен и полезен, но имеются небольшие недочёты.": 4,
    "Сервис идеален.": 4,
}

rating_options = {
    "Неудовлетворительно": 1,
    "Удовлетворительно": 2,
    "Хорошо": 3,
    "Очень хорошо": 4,
    "Отлично": 5,
}

feeling_options = {
    "Воодушевленный": 5,
    "Удовлетворенный": 4,
    "Нейтральный": 3,
    "Смущенный": 2,
    "Перегруженный информацией": 1,
}


@dp.callback_query(FeedbackCallbackData.filter(F.type == FeedbackRequest.first))
async def process_first_day(
    query: CallbackQuery, callback_data: FeedbackCallbackData, state: FSMContext
):
    _keyboard = [[KeyboardButton(text=k)] for k, _ in rating_options.items()]
    await state.set_state(Survey.rating)
    await bot.send_message(
        query.from_user.id,
        "Как бы вы оценили процесс онбординга в нашей компании?",
        reply_markup=ReplyKeyboardMarkup(keyboard=_keyboard),
    )


@dp.message(Survey.rating)
async def process_rating(message: Message, state: FSMContext) -> None:
    if message.text not in rating_options.keys():
        await message.reply("Пожалуйста выбери один из предложенных вариантов")
    else:
        _keyboard = [[KeyboardButton(text=k)] for k, _ in feeling_options.items()]
        await state.set_data(data={"rating": rating_options[message.text]})
        await state.set_state(Survey.feeling)
        await message.reply(
            text="Каково ваше эмоциональное состояние после прохождения процесса адаптации?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=_keyboard,
            ),
        )


@dp.message(Survey.feeling)
async def process_feeling(message: Message, state: FSMContext) -> None:
    if message.text not in feeling_options.keys():
        await message.reply("Пожалуйста выбери один из предложенных вариантов")
    else:
        data = await state.get_data()
        data["feeling"] = feeling_options[message.text]
        await state.set_data(data)
        await state.set_state(Survey.info)
        await bot.send_message(
            message.from_user.id,
            "Была ли предоставленная в сервисе помощь достаточной и полезной для вашей адаптации в колледже ITHub?",
            reply_markup=ReplyKeyboardRemove(),
        )


@dp.message(Survey.info)
async def process_feeling(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    data["info"] = message.text
    print(data)
    await message.reply(
        text="""
🎉 Спасибо большое за уделенное время и предоставленную обратную связь. Твоё мнение очень важно для нас, и оно помогает делать нашу компанию еще лучше!

Мы обязательно учтем твои замечания и предложения. Помни, что ты всегда можешь обратиться ко мне за помощью или дополнительной информацией.

Желаю тебе успешного дня и вдохновения в работе!"""
    )


async def main() -> None:
    # await request_feedback(test_user_id, "Максим Ледаков")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
