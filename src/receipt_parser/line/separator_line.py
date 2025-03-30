import re
from .abstract_line import AbstractLine


class SeparatorLine(AbstractLine):
    regex = re.compile(
        r"^={9,}$",
        re.IGNORECASE,
    )

    def __init__(self):
        pass

    @classmethod
    def create(cls, line: str):
        match_obj = cls.match(line)
        if match_obj:
            return cls()
        return None

    def validate(self) -> bool:
        return True
