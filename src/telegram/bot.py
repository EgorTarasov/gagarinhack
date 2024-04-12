from telebot import TeleBot


class TelegramClient:
    def __init__(self, token: str) -> None:
        self.bot = TeleBot(token=token)

    def send_notification(self, user_id: int, message: str):
        self.bot.send_message(user_id, message)
