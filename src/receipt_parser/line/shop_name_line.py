import re
from .abstract_line import AbstractLine


class ShopNameLine(AbstractLine):
    regex = re.compile(
        r"^(produit au consommateur\s)?(?P<shop_name>(MONO|MONOP)\s[a-z\s]+)$",
        re.IGNORECASE,
    )

    shop_name: str

    def __init__(self, shop_name: str):
        self.shop_name = shop_name

    @classmethod
    def create(cls, line: str):
        match_obj = cls.match(line)
        if match_obj:
            data = match_obj.groupdict()
            return cls(**data)
        return None

    def validate(self) -> bool:
        return "MONO" in self.shop_name
