from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        pass

    def validate_amount(self, amount: float) -> bool:
        return amount > 0

class CreditCardProcessor(PaymentProcessor):

    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def process_payment(self, amount) -> bool:
        if not self.validate_amount(amount):
            return False
        print(f"Processing ${amount} via credit card")
        return True
    
    def refund(self, transaction_id: str) -> bool:
        print(f"Refunding transaction {transaction_id} via credit card")
        return True

class PayPalProcessor(PaymentProcessor):

    def process_payment(self, amount) -> bool:
        if not self.validate_amount(amount):
            return False
        print(f"Processing ${amount} via PayPal")
        return True
    
    def refund(self, transaction_id: str) -> bool:
        print(f"Refunding transaction {transaction_id} via PayPal")
        return True

# Usage - polymorphism
def checkout(processor: PaymentProcessor, amount: float):
    return processor.process_payment(amount)

credit_card = CreditCardProcessor("api_key_123")
paypal = PayPalProcessor()

checkout(credit_card, 100.0)
checkout(paypal, 100.0)




