import re
from .abstract_line import AbstractLine


class PricePerKiloLine(AbstractLine):
    regex = re.compile(
        r"^(?P<weight>\d+\.\d{2,4})\s?kg(?:[a-z\s]+)(?P<price>\d+[.,]\d{2})\s?€\/kg$",
        re.IGNORECASE,
    )

    weight: float
    price: float

    def __init__(self, weight: str, price: str):
        self.weight = float(weight)
        self.price = float(price)

    @classmethod
    def create(cls, line: str):
        match_obj = cls.match(line)
        if match_obj:
            data = match_obj.groupdict()
            return cls(**data)
        return None

    def validate(self) -> bool:
        return True
