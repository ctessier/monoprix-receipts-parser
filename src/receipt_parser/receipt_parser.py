import json

from .receipt import Receipt
from .line import (
    TitleLine,
    SeparatorLine,
    DatetimeLine,
    CategoryLine,
    ItemLine,
    PricePerKiloLine,
)

LINE_TYPES = [
    TitleLine,
    SeparatorLine,
    DatetimeLine,
    CategoryLine,
    ItemLine,
    PricePerKiloLine,
]


class ReceiptParser:
    @classmethod
    def parse(cls, content: str):
        lines = content.splitlines()

        receipt = Receipt()

        for line in lines:
            line = line.strip()
            parsed_line = None
            for line_type in LINE_TYPES:
                if line_type.can_parse(line):
                    parsed_line = line_type.create(line)
                    if parsed_line.validate():
                        break
                    else:
                        parsed_line = None

            if parsed_line is not None:
                match type(parsed_line).__name__:
                    case "TitleLine":
                        receipt.next_stage(parsed_line.title)
                    case "SeparatorLine":
                        receipt.next_stage(None)
                    case "DatetimeLine":
                        receipt.datetime = parsed_line.datetime
                    case "CategoryLine":
                        receipt.set_current_category(parsed_line.name)
                    case "ItemLine":
                        receipt.apply_item(parsed_line)
                    case "PricePerKiloLine":
                        receipt.apply_price_per_kilo(**parsed_line.__dict__)

        for article in receipt.articles:
            print(json.dumps(article.__dict__, indent=4))
        for discount in receipt.discounts:
            print(json.dumps(discount.__dict__, indent=4))
        for payment in receipt.payments:
            print(json.dumps(payment.__dict__, indent=4))

        print(receipt.datetime, receipt.total_cost, receipt.total_discount)
