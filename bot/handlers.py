import uuid

from aiogram import F, Router
from aiogram.types import FSInputFile, Message

from bot.services.sheets import GoogleSheetsLogger
from bot.services.transcription import WhisperTranscriber
from bot.services.translation import GoogleTranslateService
from bot.services.video import VideoService


router = Router()


class HandlerDeps:
    def __init__(
        self,
        video_service: VideoService,
        transcriber: WhisperTranscriber,
        translator: GoogleTranslateService,
        sheets_logger: GoogleSheetsLogger,
    ) -> None:
        self.video_service = video_service
        self.transcriber = transcriber
        self.translator = translator
        self.sheets_logger = sheets_logger


deps: HandlerDeps | None = None


def configure(dependencies: HandlerDeps) -> None:
    global deps
    deps = dependencies


@router.message(F.text == "/start")
async def start(message: Message) -> None:
    await message.answer(
        "Привет! Пришли ссылку на видео.\n"
        "Я скачаю видео, сделаю транскрипцию через Whisper, переведу через Google Translate "
        "и отправлю готовый перевод в .txt файле."
    )


@router.message(F.text)
async def process_video_link(message: Message) -> None:
    if deps is None:
        raise RuntimeError("Dependencies are not configured")

    link = (message.text or "").strip()
    if not link.startswith(("http://", "https://")):
        await message.answer("Отправь корректную ссылку на видео (http/https).")
        return

    job_id = str(uuid.uuid4())
    await message.answer("Сохраняю ссылку и начинаю обработку…")

    deps.sheets_logger.append_link(message.from_user.id, link, status="queued")

    source_video = None
    try:
        source_video = deps.video_service.download_video(link, job_id)
        await message.answer("Видео скачано, запускаю транскрипцию Whisper…")

        transcription = deps.transcriber.transcribe(source_video)
        await message.answer("Транскрипция готова, перевожу текст…")

        translated_text = deps.translator.translate(transcription.text)

        text_file = deps.video_service.temp_dir / f"{job_id}_translated.txt"
        text_file.write_text(translated_text, encoding="utf-8")

        await message.answer_document(
            FSInputFile(str(text_file)),
            caption="Готово ✅ Вот сценарий перевода в TXT.",
        )
        deps.sheets_logger.append_link(message.from_user.id, link, status="completed")
    except Exception as exc:
        deps.sheets_logger.append_link(message.from_user.id, link, status="failed")
        await message.answer(f"Не удалось обработать видео. Детали: {exc}")
    finally:
        if source_video is not None:
            deps.video_service.cleanup(str(source_video))
