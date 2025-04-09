import re
import cloudscraper
from urllib.parse import unquote
from datetime import datetime


class MonoprixClient:
    def __init__(self, email: str, password: str):
        self.session = cloudscraper.create_scraper()
        self.client_id = "1UdlANOVt4FdstGpM6Kn"
        self.email = email
        self.password = password
        self.tkn = None
        self.r5_token = None
        print(email, password)

    def __login(self):
        url = "https://sso.monoprix.fr/identity/v1/password/login"
        payload = {
            "client_id": self.client_id,
            "email": self.email,
            "password": self.password,
            "scope": "openid profile email phone offline_access address full_write",
        }
        response = self.session.post(
            url,
            json=payload,
        )
        response.raise_for_status()
        self.tkn = response.json().get("tkn")
        if not self.tkn:
            raise ValueError("Login failed: tkn not found in response")

    def __get_authorize_token(self):
        if not self.tkn:
            self.__login()

        url = (
            "https://sso.monoprix.fr/oauth/authorize?"
            f"client_id={self.client_id}&"
            "response_type=token&"
            "redirect_uri=https%3A%2F%2Fclient.monoprix.fr%2Fmonoprix-shopping%2Fpost-login&"
            "scope=openid%20profile%20email%20phone%20offline_access%20address%20full_write&"
            "display=page&"
            f"tkn={self.tkn}"
        )
        response = self.session.get(url, allow_redirects=False)
        if "location" not in response.headers:
            raise ValueError("Authorization failed: Location header not found")

        location = unquote(response.headers["location"])
        match = re.search(r"[#?&]id_token=([^&]+)", location)
        if not match:
            raise ValueError(
                "Authorization failed: id_token not found in location header"
            )

        self.r5_token = match.group(1)

    def get_receipts(self, start_date: datetime, limit=10):
        if not self.r5_token:
            self.__get_authorize_token()

        url = "https://client.monoprix.fr/api/client/get-receipts"
        headers = {"R5-Token": self.r5_token, "Application-Caller": "monoprix-shopping"}
        params = {
            "limit": limit,
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": "undefined",
        }

        response = self.session.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json().get("receipts", [])

    def download_receipt(self, receipt_id: str):
        url = "https://client.monoprix.fr/api/client/get-receipt-bill"
        headers = {"R5-Token": self.r5_token, "Application-Caller": "monoprix-shopping"}
        params = {"receiptId": receipt_id, "receiptType": "store"}
        response = self.session.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.content
