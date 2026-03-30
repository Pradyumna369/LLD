class Vehicle:

    def __init__(self, brand: str, model: str, year: int):
        self.brand = brand
        self.model = model
        self.year = year

    def start(self):
        return f"{self.brand} {self.model} started."

    def stop(self):
        return f"{self.brand} {self.model} stopped."

    def get_info(self):
        return f"{self.brand} {self.model} ({self.year})"

class Car(Vehicle):
    def __init__(self, brand: str, model: str, year: int, num_doors: int):
        super().__init__(brand, model, year)    # Call parent __init__
        self.num_doors = num_doors
    
    def honk(self):
        return "Beep Beep!"

class Motorcycle(Vehicle):
    def __init__(self, brand: str, model: str, year: int, bike_type: str):
        super().__init__(brand, model, year)
        self.bike_type = bike_type
    
    def wheelie(self):
        return "Doing a wheelie!"

car = Car("Toyota", "Camry", 2020, 4)
print(car.start())
print(car.get_info())

motorcycle = Motorcycle("Yamaha", "YZF-R3", 2021, "Sport")
print(motorcycle.start())


