import re

from abc import ABC, abstractmethod


class AbstractLine(ABC):
    regex: re.Pattern

    @classmethod
    def match(cls, line: str) -> re.Match:
        return cls.regex.match(line)

    @classmethod
    def can_parse(cls, line: str) -> bool:
        return bool(cls.match(line))

    @classmethod
    @abstractmethod
    def create(cls, line: str):
        pass

    @abstractmethod
    def validate(self) -> bool:
        pass
