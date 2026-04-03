# Observer pattern is used to notify multiple objects of a state change. State pushes to observers without
# knowing observer details

from abc import ABC, abstractmethod
from datetime import datetime

# ====== OBSERVER INTERFACE ======
class OrderObserver(ABC):
    @abstractmethod
    def update(self, order_id: str, status: str, message: str):
        pass


# ======= SUBJECT INTERFACE ========
class OrderSubject(ABC):
    @abstractmethod
    def attach(self, observer: OrderObserver):
        pass

    @abstractmethod
    def detach(self, observer: OrderObserver):
        pass

    @abstractmethod
    def notify(self, status: str, message: str):
        pass

# ========= CONCRETE OBSERVERS ============
class EmailNotifier(OrderObserver):
    def __init__(self, email: str):
        self.email = email
    
    def update(self, order_id: str, status: str, message: str):
        print(f"[EMAIL -> {self.email}] Order {order_id} | "
              f"Status: {status} | message")

class SMSNotifier(OrderObserver):
    def __init__(self, phone: str):
        self.phone = phone
    
    def update(self, order_id: str, status: str, message: str):
        print(f"[SMS -> {self.phone}] Order {order_id} is now {status}")

class InventorySystem(OrderObserver):
    def update(self, order_id: str, status: str, message: str):
        if status == "CONFIRMED":
            print(f"[INVENTORY] Reserving stock for order {order_id}")
        elif status == "CANCELLED":
            print(f"[INVENTORY] Releasing stock for order {order_id}")


class AnalyticsDashboard(OrderObserver):
    def __init__(self):
        self.events = []

    def update(self, order_id: str, status: str, message: str):
        event = {
            "order_id": order_id,
            "status": status,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        self.events.append(event)
        print(f"[ANALYTICS] Event logged: {event}")

# ======= SUBJECT ========
# The object being observed - the one whose state changes are others interested in. This acts like a publisher.
class Order(OrderSubject):
    def __init__(self, order_id: str, item: str):
        self.order_id = order_id
        self.item = item
        self.status = "CREATED"
        self._observers = []        # composition — order owns its observer list

    def attach(self, observer: OrderObserver):
        self._observers.append(observer)
        print(f"Observer {observer.__class__.__name__} attached")

    def detach(self, observer: OrderObserver):
        self._observers.remove(observer)
        print(f"Observer {observer.__class__.__name__} detached")

    def notify(self, status: str, message: str):
        for observer in self._observers:
            observer.update(self.order_id, status, message)
    
    # ── state changes trigger notify ──
    def confirm(self):
        self.status = "CONFIRMED"
        self.notify("CONFIRMED", f"{self.item} order confirmed")

    def ship(self):
        self.status = "SHIPPED"
        self.notify("SHIPPED", f"{self.item} has been shipped")

    def deliver(self):
        self.status = "DELIVERED"
        self.notify("DELIVERED", f"{self.item} delivered successfully")

    def cancel(self):
        self.status = "CANCELLED"
        self.notify("CANCELLED", f"{self.item} order cancelled")

# ======== USAGE ==========
order = Order("ORD-001", "Laptop")

# attach observers
email     = EmailNotifier("alice@example.com")
sms       = SMSNotifier("+1234567890")
inventory = InventorySystem()
analytics = AnalyticsDashboard()

order.attach(email)
order.attach(sms)
order.attach(inventory)
order.attach(analytics)

print("\n--- Order Confirmed ---")
order.confirm()

print("\n--- Order Shipped ---")
order.ship()

# detach SMS — user unsubscribed from SMS updates
print("\n--- User unsubscribed from SMS ---")
order.detach(sms)

print("\n--- Order Delivered ---")
order.deliver()