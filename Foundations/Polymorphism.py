# Polymorphism through inheritance
class Notification:
    def send(self, message: str) -> bool:
        raise NotImplementedError("Subclass must implement send()")

class EmailNotification(Notification):
    def __init__(self, recipient: str):
        self.recipient = recipient

    def send(self, message: str) -> bool:
        print(f"Sending email to {self.recipient}: {message}")
        return True

class SMSNotification(Notification):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number
    
    def send(self, message: str) -> bool:
        print(f"Sending SMS to {self.phone_number}: {message[:50]}...")
        return True

class PushNotification(Notification):
    def __init__(self, device_id: str):
        self.device_id = device_id
    
    def send(self, message: str) -> bool:
        print(f"Sending push to device {self.device_id}: {message}")
        return True

class NotificationService:
    def __init__(self):
        self.notifications = []
    
    def add_notification(self, notification: Notification):
        self.notifications.append(notification)
    
    def broadcast(self, message: str):
        for notification in self.notifications:
            notification.send(message)  # Doesnt care which notification type is called. All respond to send() differently.

service = NotificationService()
service.add_notification(EmailNotification("user@example.com"))
service.add_notification(SMSNotification("+1234567890"))
service.add_notification(PushNotification("device-123"))

service.broadcast("Your order has been shipped!")

