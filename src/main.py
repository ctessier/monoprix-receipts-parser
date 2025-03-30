from pdf_reader import PdfReader
from receipt_parser import ReceiptParser


def main():
    content = PdfReader.read("../data/d4596d88-fdde-40f2-a719-d25ec4cd3c81.pdf")

    ReceiptParser().parse(content)


if __name__ == "__main__":
    main()
