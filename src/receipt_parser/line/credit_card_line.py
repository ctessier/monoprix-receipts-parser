import re
from .abstract_line import AbstractLine


class CreditCardLine(AbstractLine):
    regex = re.compile(
        r"^(?P<card_number>\*{12}\d{4})$",
        re.IGNORECASE,
    )

    card_number: str

    def __init__(self, card_number: str):
        self.card_number = card_number

    @classmethod
    def create(cls, line: str):
        match_obj = cls.match(line)
        if match_obj:
            data = match_obj.groupdict()
            return cls(**data)
        return None

    def validate(self) -> bool:
        return "************" in self.card_number
