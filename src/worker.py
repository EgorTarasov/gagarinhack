from celery import Celery
from config import Config
from utils.email import EmailClient
# from telegram import bot


# FIXME: worker invalid config
cfg = Config()  # type: ignore

celery_client = Celery(
    "background",
    broker=cfg.rabbitmq_url,
)


email_client = EmailClient(
    mail_user=cfg.mail_user,
    mail_password=cfg.mail_password,
    templates_path="../templates",
)


@celery_client.task
def send_email_recovery_code(
    email: str, first_name: str, last_name: str, code: str
) -> None:
    """Sends email with password recovery link"""
    subject = "Смена пароля"
    template = "password_recover.jinja"
    link_on_password_recover = f"{cfg.app_host}/reset-password?token={code}"

    data = {
        "fullname": f"{first_name} {last_name}",
        "link_on_password_recover": link_on_password_recover,
    }
    email_client.send_mailing(email, subject, template, data)


# @celery_client.task
# def send_telegram_notification(
#     user_id: int,
#     msg: str,
# ) -> None:
#     bot.send_notification(user_id, msg)
