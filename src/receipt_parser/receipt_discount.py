class ReceiptDiscount:
    name: str
    amount: float

    def __init__(self, name: str, amount: float):
        self.name = name
        self.amount = amount
