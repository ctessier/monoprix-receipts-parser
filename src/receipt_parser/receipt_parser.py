
from .receipt import Receipt
from .line import (
    ShopNameLine,
    TitleLine,
    SeparatorLine,
    DatetimeLine,
    CategoryLine,
    ItemLine,
    PricePerKiloLine,
    CreditCardLine,
)

LINE_TYPES = [
    ShopNameLine,
    TitleLine,
    SeparatorLine,
    DatetimeLine,
    CategoryLine,
    ItemLine,
    PricePerKiloLine,
    CreditCardLine,
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
                    case "ShopNameLine":
                        receipt.shop_name = parsed_line.shop_name
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
                    case "CreditCardLine":
                        receipt.apply_credit_card(parsed_line)

        return receipt
