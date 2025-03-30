from typing import Optional


class ReceiptArticle:
    name: str
    quantity: float
    unit_price: float
    total_cost: float
    category: str
    total_discount: float = 0
    cost_without_discount: float = 0
    discount_name: Optional[str] = None

    def __init__(
        self,
        name: str,
        category: str,
        total_price: float,
        unit_price: float | None,
        quantity: int,
    ):
        self.name = name
        self.unit_price = unit_price
        self.total_cost = total_price
        self.cost_without_discount = total_price
        self.quantity = quantity
        self.category = category

    def apply_discount(self, name: str, amount: float):
        self.discount_name = name
        self.total_discount = round(self.total_discount + amount, 3)
        self.total_cost = round(self.total_cost + amount, 3)

    def apply_weight_cost(self, weight: float, price: float):
        self.quantity = weight
        if price == self.total_cost and weight != 1:
            self.unit_price = round(price / weight, 3)
        else:
            self.unit_price = price
