from typing import Literal, Optional

from datetime import datetime as dt

from .line import CreditCardLine
from .line.item_line import ItemLine
from .receipt_article import ReceiptArticle
from .receipt_discount import ReceiptDiscount
from .receipt_payment import ReceiptPayment

Stage = Literal["shop", "total", "pay", "done"]


class Receipt:
    __stage: Stage
    __current_category: str | None

    shop_name: str
    datetime: dt
    articles: list[ReceiptArticle]
    discounts: list[ReceiptDiscount]
    payments: list[ReceiptPayment]
    total_cost: float
    total_discount: float

    def __init__(self):
        self.__stage = "shop"
        self.articles = []
        self.discounts = []
        self.payments = []
        self.total_cost = 0
        self.total_discount = 0
        self.current_category = None

    def next_stage(self, title: Optional[str]):
        if title is not None:
            if "FIDELITE" in title:
                self.__stage = "done"
            if "PAIEMENT" in title:
                self.__stage = "pay"
        else:
            if self.__stage == "shop":
                self.__stage = "total"

        if not self.__stage == "shop":
            self.__current_category = None

    def set_current_category(self, category: str | None):
        if self.__stage == "shop":
            self.current_category = category

    def apply_price_per_kilo(self, weight: float, price: float):
        if self.__stage == "shop":
            last_article = self.articles[-1]
            last_article.apply_weight_cost(weight, price)

    def apply_item(self, item: ItemLine):
        if self.__stage == "shop":
            if item.price_1 > 0:
                self.__add_article(item)
            else:
                self.__apply_article_discount(item)
        elif self.__stage == "total":
            if item.price_1 < 0 and "TOTAL" not in item.name:
                self.__apply_total_discount(item)
        elif self.__stage == "pay":
            if item.price_1 > 0:
                self.__apply_payment(item)

    def apply_credit_card(self, credit_card: CreditCardLine):
        for payment in self.payments:
            if payment.name in ["CARTE BANCAIRE", "CARTE", "CB EMV", "CARTE GENERIQUE"]:
                payment.card_number = credit_card.card_number
                break

    def __add_article(self, item: ItemLine):
        article = ReceiptArticle(
            name=item.name,
            category=self.current_category,
            quantity=item.quantity,
            unit_price=item.price_1,
            total_price=item.price_2 if item.price_2 is not None else item.price_1,
        )
        self.articles.append(article)
        self.total_cost = round(self.total_cost + article.total_cost, 3)

    def __apply_article_discount(self, item: ItemLine):
        self.articles[-1].apply_discount(name=item.name, amount=item.price_1)

    def __apply_total_discount(self, item: ItemLine):
        name = item.name
        amount = item.price_1
        self.total_discount = round(self.total_discount + amount, 3)
        self.total_cost = round(self.total_cost + amount, 3)
        self.discounts.append(ReceiptDiscount(name, amount))

    def __apply_payment(self, item: ItemLine):
        self.payments.append(
            ReceiptPayment(
                name=item.name,
                amount=item.price_1,
            )
        )
