import asyncio

from aiogram import Bot, Dispatcher

from bot.config import load_settings
from bot.handlers import HandlerDeps, configure, router
from bot.services.sheets import GoogleSheetsLogger
from bot.services.storage import InMemoryJobStore
from bot.services.transcription import WhisperTranscriber
from bot.services.translation import LibreTranslator
from bot.services.video import VideoService


async def main() -> None:
    settings = load_settings()

    bot = Bot(token=settings.telegram_token)
    dp = Dispatcher()

    configure(
        HandlerDeps(
            store=InMemoryJobStore(),
            video_service=VideoService(settings.temp_dir),
            transcriber=WhisperTranscriber(model_name=settings.whisper_model, language=settings.whisper_language),
            translator=LibreTranslator(
                base_url=settings.libretranslate_url,
                source_lang=settings.source_lang,
                target_lang=settings.target_lang,
                api_key=settings.libretranslate_api_key,
            ),
            sheets_logger=GoogleSheetsLogger(
                credentials_path=settings.sheets_credentials_path,
                spreadsheet_id=settings.sheets_spreadsheet_id,
                worksheet_name=settings.sheets_worksheet_name,
            ),
            max_preview_chars=settings.max_preview_chars,
        )
    )

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
