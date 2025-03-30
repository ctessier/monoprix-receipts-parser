import re
from datetime import datetime as dt
from .abstract_line import AbstractLine


class DatetimeLine(AbstractLine):
    regex = re.compile(
        r"^(?P<datetime>\d{2}\/\d{2}\/20\d{2}\s\d{2}:\d{2})",
        re.IGNORECASE,
    )

    datetime: dt

    def __init__(self, datetime: str):
        self.datetime = dt.strptime(datetime, "%d/%m/%Y %H:%M")

    @classmethod
    def create(cls, line: str):
        match_obj = cls.match(line)
        if match_obj:
            data = match_obj.groupdict()
            return cls(**data)
        return None

    def validate(self) -> bool:
        return self.datetime < dt.now()
