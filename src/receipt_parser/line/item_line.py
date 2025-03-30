import re
from typing import Optional

from .abstract_line import AbstractLine


class ItemLine(AbstractLine):
    regex = re.compile(
        r"^(?:(?P<quantity>\d+)(?:X)\s+)?(?P<name>.+?)\s+(?P<price_1>-?\d+[.,]\d{2})€(?:\s+(?P<price_2>-?\d+[.,]\d{2})€)?$",
        re.IGNORECASE,
    )

    name: str
    quantity: int
    price_1: float
    price_2: float

    def __init__(
        self, name: str, price_1: str, price_2: Optional[str], quantity: Optional[str]
    ):
        self.name = name
        self.quantity = int(quantity if quantity is not None else 1)
        self.price_1 = float(price_1.replace(",", "."))
        self.price_2 = float(price_2.replace(",", ".")) if price_2 is not None else None

    @classmethod
    def create(cls, line: str):
        match_obj = cls.match(line)
        if match_obj:
            data = match_obj.groupdict()
            return cls(**data)
        return None

    def validate(self) -> bool:
        if self.price_2 is not None:
            return self.price_1 < self.price_2 == self.price_1 * self.quantity
        return self.quantity == 1
