from constants import User
from utils import get_notifier, get_user_contact


class DecoupledNotifier:
    # doesn't know about the implementation details of the "notifier"
    def notify_user(self, user: User, message: str):
        notifier = get_notifier(user.notification_preference)
        notifier.notify(receiver=get_user_contact(user), message=message)
