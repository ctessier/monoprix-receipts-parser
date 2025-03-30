import re
from .abstract_line import AbstractLine


class CategoryLine(AbstractLine):
    regex = re.compile(
        r"^(?P<name>[a-z\/\s]+)\.+$",
        re.IGNORECASE,
    )

    name: str

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def create(cls, line: str):
        match_obj = cls.match(line)
        if match_obj:
            data = match_obj.groupdict()
            return cls(**data)
        return None

    def validate(self) -> bool:
        return True
