# Strategy is a behavioural pattern that lets you define a family of algorithms, put each of them into a separate
# class, and make their objects interchangeable during runtime.

from abc import ABC, abstractmethod

# ======= STRATEGY INTERFACE =======
class ShippingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, weight_kg: float, distance_km: float) -> float:
        pass

    @abstractmethod
    def get_delivery_days(self) -> int:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

# ======== CONCRETE STRATEGIES ==========
class StandardShipping(ShippingStrategy):
    def calculate_cost(self, weight_kg: float, distance_km: float) -> float:
        return weight_kg * 0.5 + distance_km * 0.01

    def get_delivery_days(self) -> int:
        return 7
    
    def get_name(self) -> str:
        return "Standard Shipping"

class ExpressShipping(ShippingStrategy):
    def calculate_cost(self, weight_kg: float, distance_km: float) -> float:
        return weight_kg * 1.5 + distance_km * 0.01

    def get_delivery_days(self) -> int:
        return 2
    
    def get_name(self) -> str:
        return "Express Shipping"
    
class OvernightShipping(ShippingStrategy):
    def calculate_cost(self, weight_kg: float, distance_km: float) -> float:
        return weight_kg * 3.0 + distance_km * 0.01 + 20

    def get_delivery_days(self) -> int:
        return 1
    
    def get_name(self) -> str:
        return "OvernightShipping Shipping"

class FreeShipping(ShippingStrategy):
    def calculate_cost(self, weight_kg: float, distance_km: float) -> float:
        return 0.0

    def get_delivery_days(self) -> int:
        return 14

    def get_name(self) -> str:
        return "Free Shipping"

# ======= CONTEXT ========
class Order:
    def __init__(self, order_id: str, weight_kg: float, distance_km: float):
        self.order_id = order_id
        self.weight_kg = weight_kg
        self.distance_km = distance_km
        self._shipping_strategy = StandardShipping()
    
    def set_shipping_strategy(self, strategy: ShippingStrategy):
        self._shipping_strategy = strategy
    
    def get_shipping_cost(self) -> float:
        return self._shipping_strategy. calculate_cost(
            self.weight_kg, self.distance_km
        )

    def get_summary(self):
        cost = self.get_shipping_cost()
        days = self._shipping_strategy.get_delivery_days()
        name = self._shipping_strategy.get_name()
        print(f"Order {self.order_id} | {name} | "
              f"Cost: ${cost:.2f} | Delivery: {days} days")
    
# # ======== USAGE ========
# order = Order("ORD-001", weight_kg=2.5, distance_km=300)

# # default strategy
# order.get_summary()

# # swap strategy at runtime based on user choice
# order.set_shipping_strategy(ExpressShipping())
# order.get_summary()

# order.set_shipping_strategy(OvernightShipping())
# order.get_summary()

# # swap based on business rule - order over $100 gets free shipping
# order_total = 150
# if order_total > 100:
#     order.set_shipping_strategy(FreeShipping())
# order.get_summary()

# Combining it with factory pattern so that caller never touches strategy classes directly
class ShippingStrategyFactory:
    @staticmethod
    def create(shipping_type: str, order_total: float = 0) -> ShippingStrategy:
        if order_total > 100:
            return FreeShipping()

        strategies = {
            "standard"  : lambda: StandardShipping(),
            "express"   : lambda: ExpressShipping(),
            "overnight" : lambda: OvernightShipping(),
        }

        creator = strategies.get(shipping_type.lower())

        if not creator:
            raise ValueError(f"Unknown shipping type: {shipping_type}")
        return creator()

# ======== USAGE =========
order = Order("ORD-001", weight_kg=2.5, distance_km=300)

# caller never touches concrete strategy classes directly
strategy = ShippingStrategyFactory.create("express", order_total=80)
order.set_shipping_strategy(strategy)
order.get_summary()

# business rule handled inside factory
strategy = ShippingStrategyFactory.create('express', order_total=150)
order.set_shipping_strategy(strategy)
order.get_summary()