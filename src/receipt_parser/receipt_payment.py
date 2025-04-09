from typing import Optional


class ReceiptPayment:
    name: str
    card_number: Optional[str]
    amount: float

    def __init__(self, name: str, amount: float):
        self.name = name
        self.amount = amount
        self.card_number = None
