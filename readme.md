# Dependency Inversion, Dependency Injection and Inversion of Control
I'm always mixing up and confusing these terms! So read some articles, 
and made a summary + code examples here for myself to learn these concepts once
and for all!



## Dependency Inversion
remember SOLID? well, Dependency Inversion is the "D" in SOLID. 

A refresher:
- **S**ingle Responsibility
- **O**pen-Close Principle
- **L**iskov's substitution Principle
- **I**nterface Segregation Principle
- **D**ependency Inversion Principle


Inversion of Dependency is a *principle*. It simply says 
1. high-level module should
not depend on low-level module. Instead, both should depend on *abstractions*. 
2. Abstractions should not depend on details, like concrete implementations.


## Dependency Injection
Dependency Injection is a *pattern*. By implementing this pattern, we can "invert"
the dependency between classes, and thus, achieve Dependency Inversion!

How does the pattern work?

Imagine class A depends on class B. It needs class B to do something.
One way to achieve this is having class A instantiating class B in its code. 
So now:
 - class A needs to know how to configure class B
 - it's difficult to unit test class A
 - if something in class B configuration changes, we have to change class A as well


Instead of allowing class A to instantiate class B, we feed class A an instance of 
class B, that is, we *inject* class A with an instance of class B. So now:
- class A doesn't need to know how to configure class B
- we can easily unit test class A


Even better, we can add an Interface that class B implements, call it *IB*,
and make class A depend on IB, instead of class B. This way, any class that 
implements the functionalities in IB which class A needs, can be used by class A!

how to do the injection
- constructor injection
- interface injection
- setter injection

## Inversion of Control
IoC is a design principle.
In a traditional procedural application, the flow of the program is top-to-bottom. 
The program starts, instantiates the classes it depends on and so on.

The idea of the IoC that we can have a framework/container that does all the binding behind
the scene, and only calls our application when needed. It takes care of the instantiation
of the classes. The classes don't need to create instances of the other classes they 
depend on, instead this task is delegated to the framework/container.

Imagine class A depends on class B.

- To-to-bottom
  - the flow of the program starts and reaches class A
  - class A depends on class B, so it instantiates class B
- IoC
  - we use a dependency injection technique to pass an already-created instance of B to class A
  - the flow of the program is now "inverted" --> Inversion of Control


*dependency injection is not the only way of achieving IoC*
> We can achieve Inversion of Control through various mechanisms such as: **Strategy design pattern, Service Locator pattern, Factory pattern, and Dependency Injection (DI)**
([Baeldung](https://www.baeldung.com/inversion-control-and-dependency-injection-in-spring))



## Example
I tried to come up with a bad coupled example, and fix it.


Say I have a system where I need to send out notifications to my users.

One way to do it is like this
```python
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
```
(`notify_user` is too simple to belong to a class IMO, could just be a uitl method, but this is an example)

`CoupledNotification` has to know about the details of SMTP library. If I want to add more ways of notifying
my users, for example, sending text messages, this class would become dependent to even more low-level details.


Steps to make this a little better:
- add an interface `INotifier` that has `notify` method
- move the emailing part to a separate class `EmailNotifier` that implements `INotifier`
- `EmailNotifier` will use SMTP
  - if any details related to how the email communication implementation needs to change, all is isolated in `EmailNotifier`
- Other ways of notification like text messages can be added and used as plug-and-play as long as they implement methods of `INotifier`


```python
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
```

- `DecoupledNotification` depends on `INotifier` 
- anything that implements `INotifier` can do the job for `DecoupledNotification`

```python
class DecoupledNotifier:
    # doesn't know about the implementation details of the "notifier"
    def notify_user(self, user: User, message: str):
        notifier = get_notifier(user.notification_preference)
        notifier.notify(receiver=get_user_contact(user), message=message)
```

and we managed to "invert" the dependency of `CoupledNotification` to the low-level SMTP library using the 
interface injection technique.