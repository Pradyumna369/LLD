from abc import ABC, abstractmethod

# ======= ABSTRACT PRODUCT ======= #
class Vehicle(ABC):
    def __init__(self, brand: str, model: str):
        self.brand = brand
        self.model = model
    
    @abstractmethod
    def get_specs(self) -> str:
        pass

    @abstractmethod
    def start_engine(self) -> str:
        pass

    def __str__(self):
        return f"{self.brand} {self.model}"

# =========== CONCRETE PRODUCTS =========== #
class Car(Vehicle):
    def __init__(self, brand: str, model: str, num_doors: int):
        super().__init__(brand, model)
        self.num_doors = num_doors
    
    def get_specs(self) -> str:
        return f"Car | Doors: {self.num_doors}"

    def start_engine(self) -> str:
        return f"{self} - car engine starts: vroom!"

class Truck(Vehicle):
    def __init__(self, brand: str, model: str, payload_tons: float):
        super().__init__(brand, model)
        self.payload_tons = payload_tons
    
    def get_specs(self) -> str:
        return f"Truck | Payload: {self.payload_tons}"

    def start_engine(self) -> str:
        return f"{self} - truck engine starts: RUMBLE!"

class Motorcycle(Vehicle):
    def __init__(self, brand: str, model: str, bike_type: str):
        super().__init__(brand, model)
        self.bike_type = bike_type
    
    def get_specs(self) -> str:
        return f"Motorcycle | Type: {self.bike_type}"
    
    def start_engine(self) -> str:
        return f"{self} - bike engine starts: VROOMM!"

# ====== Factory ====== #
# Factory to take a vehicle_type and return the right object.
# The knowledge of Car, Truck, Motorcycle is centralized here.
class VehicleFactory:
    @staticmethod
    # Using dictionary dispatch instead of if/else chain. 
    # Cleaner and adding a new vechicle type is just adding one line to dic
    def create(vehicle_type: str, brand: str, model: str, **kwargs) -> Vehicle:
        factories = {
            "car"   :   lambda: Car(brand, model, kwargs.get("num_doors", 4)),
            "truck" :   lambda: Truck(brand, model, kwargs.get("payload_tons", 1.0)),
            "motorcycle"    : lambda: Motorcycle(brand, model, kwargs.get("bike_type", "standard"))
        }

        creator = factories.get(vehicle_type.lower())
        if not creator:
            raise ValueError(f"Unknown Vehicle Type: {vehicle_type}."
                                f"Supported: {list(factories.keys())}")

        return creator()

# ====== Usage ====== #
# The caller need not know about concrete classes. Only the factory knows about them.
# The caller only depends on VehicleFactory and Vehicle - never on Car, Truck or Motorcycle directly.
car = VehicleFactory.create("car", "Toyota", "Camry", num_doors=4)
truck = VehicleFactory.create("truck", "Ford", "F-150", payload_tons=0.9)
bike = VehicleFactory.create("motorcycle", "Honda", "CBR600", bike_type="sport")

vehicles = [car, truck, bike]
for v in vehicles:
    print(v.get_specs())
    print(v.start_engine())
    print()


# Mental model
# Like a restaurant kitchen
# Caller = customer, orders "pasta" - doesn't know the recepie
# Factory = kitchen, knows exactly how to make pasta
# Concrete classes = the actual dish being assembled
# 
# The kitchen has to know the recpie. The customer never should.

