import uuid

from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, Message

from bot.keyboards import review_keyboard
from bot.services.sheets import GoogleSheetsLogger
from bot.services.storage import InMemoryJobStore, JobStatus, TranslationJob
from bot.services.transcription import WhisperTranscriber
from bot.services.translation import LibreTranslator
from bot.services.video import VideoService


router = Router()


class HandlerDeps:
    def __init__(
        self,
        store: InMemoryJobStore,
        video_service: VideoService,
        transcriber: WhisperTranscriber,
        translator: LibreTranslator,
        sheets_logger: GoogleSheetsLogger,
        max_preview_chars: int,
    ) -> None:
        self.store = store
        self.video_service = video_service
        self.transcriber = transcriber
        self.translator = translator
        self.sheets_logger = sheets_logger
        self.max_preview_chars = max_preview_chars


deps: HandlerDeps | None = None


def configure(dependencies: HandlerDeps) -> None:
    global deps
    deps = dependencies


@router.message(F.text == "/start")
async def start(message: Message) -> None:
    await message.answer(
        "Привет! Пришли ссылку на видео.\n"
        "Я извлеку аудио, сделаю транскрипцию, переведу текст через LibreTranslate "
        "и отправлю на проверку."
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

    audio_path = deps.video_service.download_audio(link, job_id)
    await message.answer("Аудио готово, запускаю транскрипцию…")

    transcript = deps.transcriber.transcribe(audio_path)
    await message.answer("Транскрипция готова, запускаю перевод…")

    translated_text = deps.translator.translate(transcript)

    job = TranslationJob(
        job_id=job_id,
        user_id=message.from_user.id,
        source_url=link,
        transcript=transcript,
        translated_text=translated_text,
        media_path=str(audio_path),
    )
    deps.store.put(job)

    preview = translated_text[: deps.max_preview_chars]
    await message.answer(
        f"Пруф перевода (первые {deps.max_preview_chars} символов):\n\n{preview}",
        reply_markup=review_keyboard(job_id),
    )


@router.callback_query(F.data.startswith("approve:"))
async def approve_translation(query: CallbackQuery) -> None:
    if deps is None:
        raise RuntimeError("Dependencies are not configured")

    job_id = query.data.split(":", 1)[1]
    job = deps.store.get(job_id)
    if not job:
        await query.answer("Задача уже неактуальна", show_alert=True)
        return

    job.status = JobStatus.approved
    deps.sheets_logger.append_link(job.user_id, job.source_url, status="approved")

    text_file = f"{job_id}_translated.txt"
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(job.translated_text)

    await query.message.answer_document(FSInputFile(text_file), caption="Перевод подтверждён.")
    await query.answer("Готово")


@router.callback_query(F.data.startswith("reject:"))
async def reject_translation(query: CallbackQuery) -> None:
    if deps is None:
        raise RuntimeError("Dependencies are not configured")

    job_id = query.data.split(":", 1)[1]
    job = deps.store.get(job_id)
    if not job:
        await query.answer("Задача уже неактуальна", show_alert=True)
        return

    job.status = JobStatus.rejected
    deps.sheets_logger.append_link(job.user_id, job.source_url, status="rejected")
    deps.video_service.cleanup(job.media_path)
    deps.store.delete(job_id)

    await query.message.answer("Отклонено. Файл удалён.")
    await query.answer("Удалено")
