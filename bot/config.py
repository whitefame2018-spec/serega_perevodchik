from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    telegram_token: str
    whisper_model: str
    whisper_language: str | None
    source_lang: str
    target_lang: str
    temp_dir: str
    max_preview_chars: int
    sheets_credentials_path: str | None
    sheets_spreadsheet_id: str | None
    sheets_worksheet_name: str


def load_settings() -> Settings:
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "")

    if not telegram_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is required")

    whisper_language = os.getenv("WHISPER_LANGUAGE")

    return Settings(
        telegram_token=telegram_token,
        whisper_model=os.getenv("WHISPER_MODEL", "base"),
        whisper_language=whisper_language if whisper_language else None,
        source_lang=os.getenv("SOURCE_LANG", "auto"),
        target_lang=os.getenv("TARGET_LANG", "ru"),
        temp_dir=os.getenv("TEMP_DIR", "./tmp"),
        max_preview_chars=int(os.getenv("MAX_PREVIEW_CHARS", "1400")),
        sheets_credentials_path=os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH"),
        sheets_spreadsheet_id=os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID"),
        sheets_worksheet_name=os.getenv("GOOGLE_SHEETS_WORKSHEET", "Sheet1"),
    )
