import time
from utils.email import EmailClient
from config import cfg

email_client = EmailClient(
    cfg.mail_user, cfg.mail_password, cfg.mail_host, cfg.mail_port
)


async def send_email_recovery_code(
    email: str, first_name: str, last_name: str, code: str
) -> None:
    """Sends email with password recovery link"""
    subject = "Смена пароля"
    template = "password_recover.jinja"
    link_on_password_recover = f"localhost:8000/reset-password?token={code}"
    print(f"sending email {time.time()}")
    data = {
        "fullname": f"{first_name} {last_name}",
        "link_on_password_recover": link_on_password_recover,
    }
    email_client.send_mailing(email, subject, template, data)

