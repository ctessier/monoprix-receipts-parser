from PyPDF2 import PdfReader as PyPDF2Reader


class PdfReader:
    @classmethod
    def read(cls, path: str):
        reader = PyPDF2Reader(path)
        content = ""

        for page in reader.pages:
            content = content + page.extract_text()

        return content
