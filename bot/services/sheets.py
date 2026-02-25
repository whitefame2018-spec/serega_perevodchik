from datetime import datetime, timezone

import gspread
from google.oauth2.service_account import Credentials


class GoogleSheetsLogger:
    def __init__(
        self,
        credentials_path: str | None,
        spreadsheet_id: str | None,
        worksheet_name: str,
    ) -> None:
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        self.worksheet_name = worksheet_name

    def append_link(self, user_id: int, link: str, status: str = "received") -> None:
        if not self.credentials_path or not self.spreadsheet_id:
            return

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(self.spreadsheet_id).worksheet(self.worksheet_name)

        sheet.append_row(
            [
                datetime.now(timezone.utc).isoformat(),
                str(user_id),
                link,
                status,
            ]
        )
