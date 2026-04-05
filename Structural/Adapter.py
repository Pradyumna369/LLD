# Adapter is a structural design pattern that allows objects with incompatible interfaces to collaborate.
# It works like a power plug adapter with different sockets for differnt countries, USA plug -> German socket.

from abc import ABC, abstractmethod

# ============ YOUR SYSTEM'S INTERFACE ============
# This is what the entire codebase expects
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float, currency: str) -> bool:
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> bool:
        pass

# ========= OWN IMPLEMENTATION ===========
# Works fine with your interface
class StripeProcessor(PaymentProcessor):
    def pay(self, amount: float, currency: str) -> bool:
        print(f"Stripe: charging {amount} {currency}")
        return True
    
    def refund(self, transaction_id: str, amount: float) -> bool:
        print(f"Stripe: refunding {amount} for {transaction_id}")
        return True

# ========== THIRD PARTY LIBRARY ===========
# can't modify this - external code. Completely different method names and signatures
class LegacyPayPalSDK:
    def make_payment(self, cents: int, currency_code: str, merchant_id: str):
        print(f"PayPal SDK: processing {cents} cents"
              f" in {currency_code} for mechant {merchant_id}")
        return {"status": "SUCCESS", "txn_id" : "PP-123"}
    
    def reverse_transaction(self, txn_id: str, cents: int):
        print(f"PayPal SDK: reversing {cents} cents for txn {txn_id}")
        return {"status": "REVERSED"}

# ========== ADAPTER ==========
# wraps the incompatible interface - translates your calls to PayPal's calls
class PayPalAdapter(PaymentProcessor):
    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id
        self.paypal = LegacyPayPalSDK()     # composition - wraps the SDK
        self.last_txn_id = None
    
    def pay(self, amount: float, currency: str) -> bool:
        # translate: float dollars -> integer cents
        cents = int(amount * 100)
        result = self.paypal.make_payment(cents, currency, self.merchant_id)
        self.last_txn_id = result.get("txn_id")
        return result.get("status") == "SUCCESS"

    def refund(self, transaction_id: str, amount: float) -> bool:
        cents = int(amount * 100)
        result = self.paypal.reverse_transaction(transaction_id, cents)
        return result.get("status") == "REVERSED"

# =========== CLIENT ==============
# only knows about PaymentProcessor - never knows about PayPal SDK
class Checkout:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor      # any PaymentProcessor works
    
    def complete_purchase(self, amount:float, currency: str):
        success = self.processor.pay(amount, currency)
        if success:
            print("Purchase complete!")
        else:
            print("Payment failed")

# =========== USAGE ============
# stripe - works natively
stripe_checkout = Checkout(StripeProcessor())
stripe_checkout.complete_purchase(99.99, "USD")

print()

# paypal - works through adapter, client has no idea
paypal_checkout = Checkout(PayPalAdapter(merchant_id="MERCHANT-001"))
paypal_checkout.complete_purchase(98.99, "USD")


