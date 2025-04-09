import json

from io import BytesIO
import requests
from config import Config
from pdf_reader import PdfReader
from receipt_parser import ReceiptParser
from monoprix import MonoprixClient


def main():
    config = Config()

    m_client = MonoprixClient(
        email=config.monoprix_email, password=config.monoprix_password
    )

    start_date = config.get_start_date()
    print(f"Fetching up to {config.limit} receipts since {start_date}")

    receipts = m_client.get_receipts(start_date=start_date, limit=config.limit)

    for receipt in receipts:
        pdf = m_client.download_receipt(receipt["id"])
        pdf_stream = BytesIO(pdf)

        parsed_receipt = ReceiptParser.parse(PdfReader.read(pdf_stream))

        print(
            f"Receipt {receipt['id']} @{parsed_receipt.shop_name}: date={parsed_receipt.datetime}, nb_articles={len(parsed_receipt.articles)}, total_price={parsed_receipt.total_cost}"
        )

        if config.webhook_url:
            payload = {
                "date": parsed_receipt.datetime.isoformat(),
                "shop": parsed_receipt.shop_name,
                "total_cost": parsed_receipt.total_cost,
                "total_discount": parsed_receipt.total_discount,
                "articles": json.dumps([p.__dict__ for p in parsed_receipt.articles]),
                "discounts": json.dumps([p.__dict__ for p in parsed_receipt.discounts]),
                "payments": json.dumps([p.__dict__ for p in parsed_receipt.payments]),
            }
            response = requests.post(
                config.webhook_url,
                json=payload,
            )
            response.raise_for_status()

        if config.verbose:
            print(json.dumps([p.__dict__ for p in parsed_receipt.articles], indent=4))
            print(json.dumps([p.__dict__ for p in parsed_receipt.discounts], indent=4))
            print(json.dumps([p.__dict__ for p in parsed_receipt.payments], indent=4))

    print(f"Done with {len(receipts)} receipts")


if __name__ == "__main__":
    main()
