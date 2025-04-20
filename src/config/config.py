import os
from datetime import datetime, timedelta
from typing import Optional


class Config:
    monoprix_email: str
    monoprix_password: str
    from_date: Optional[str]
    from_date_relative: Optional[int]
    limit: int
    webhook_url: Optional[str]
    verbose: bool

    def __init__(self):
        self.monoprix_email = os.environ.get("MONOPRIX_EMAIL")
        self.monoprix_password = os.environ.get("MONOPRIX_PASSWORD")
        self.from_date = os.environ.get("FROM_DATE")
        self.from_date_relative = (
            int(os.environ.get("FROM_DATE_RELATIVE"))
            if os.environ.get("FROM_DATE_RELATIVE") is not None
            else None
        )
        self.limit = (
            int(os.environ.get("LIMIT")) if os.environ.get("LIMIT") is not None else 5
        )
        self.webhook_url = os.environ.get("WEBHOOK_URL")
        self.verbose = (
            bool(os.environ.get("VERBOSE"))
            if os.environ.get("VERBOSE") is not None
            else False
        )
        
        if not self.monoprix_email or not self.monoprix_password:
            raise ValueError(
                "Missing required environment variables: MONOPRIX_EMAIL or MONOPRIX_PASSWORD"
            )

    def get_start_date(self):
        try:
            if self.from_date_relative is not None:
                start_date = datetime.now() + timedelta(days=self.from_date_relative)
            elif self.from_date is not None:
                start_date = datetime.fromisoformat(self.from_date)
            else:
                raise ValueError("No valid date information provided")
        except ValueError as e:
            print(f"Error converting date: {e}. Using relative date: -1")
            start_date = datetime.now() + timedelta(days=-1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            start_date = datetime.now() + timedelta(days=-1)

        return start_date
