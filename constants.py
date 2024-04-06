from dataclasses import dataclass
from enum import Enum
from typing import Optional

Settings = {
    "SMTP_SERVER_HOST": "localhost",
    "SMTP_SERVER_PORT": 234,
    "SMTP_SERVER_USERNAME": "username@host.com",
    "SMTP_SERVER_PASSWORD": "password",
    "NO_REPLY_EMAIL": "no_reply@mycompany.co",
}


class NotificationMethodEnum(Enum):
    EMAIL = "EMAIL"
    TEXT = "TEXT"


@dataclass
class User:
    email: str
    phone: Optional[str] = None
    notification_preference: NotificationMethodEnum = NotificationMethodEnum.EMAIL
