import smtplib

from constants import User, NotificationMethodEnum, Settings


class CoupledNotification:
    # this class is dependent on the details of SMTP implementation

    def notify_user(self, user: User, message: str):
        if user.notification_preference == NotificationMethodEnum.EMAIL:
            with smtplib.SMTP_SSL(host=Settings.get("SMTP_SERVER_HOST"),
                                  port=Settings.get("SMTP_SERVER_HOST")) as server:
                server.login(Settings.get("SMTP_SERVER_EMAIL"), Settings.get("SMTP_SERVER_PASSWORD"))
                server.sendmail(Settings.get("NO_REPLY_EMAIL"), user.email, message)
                return
        raise NotImplementedError(f"Notification method {user.notification_preference} not implemented!")
