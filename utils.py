import smtplib
from abc import ABCMeta, abstractmethod

from constants import NotificationMethodEnum, User, Settings


class INotifier(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def notify(self, receiver, message):
        raise NotImplementedError


class EmailNotifier(INotifier):
    _server = None

    def __init__(self):
        super().__init__()
        if not self._server:
            self._set_up_server()

    def _set_up_server(self):
        self._server =  smtplib.SMTP_SSL(Settings.get("SMTP_SERVER_HOST"), Settings.get("SMTP_SERVER_HOST"))

    def notify(self, receiver, message):
        self._send_email(Settings.get("NO_REPLY_EMAIL"), receiver, message)

    def _send_email(self, sender, receiver: str, message: str):
        print(f"Sending an email to {receiver}...")
        self._server.login(Settings.get("SMTP_SERVER_EMAIL"), Settings.get("SMTP_SERVER_PASSWORD"))
        self._server.sendmail(sender, receiver, message)


def get_notifier(medium: NotificationMethodEnum) -> INotifier:
    if medium == NotificationMethodEnum.EMAIL:
        return EmailNotifier()
    if medium == NotificationMethodEnum.TEXT:
        pass


def get_user_contact(user: User):
    if user.notification_preference == NotificationMethodEnum.EMAIL:
        return user.email
    if user.notification_preference == NotificationMethodEnum.TEXT:
        return user.phone
    raise ValueError(f"Invalid notification preference for user {user.email}!")
