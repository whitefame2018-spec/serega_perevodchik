from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def review_keyboard(job_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"approve:{job_id}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject:{job_id}"),
            ]
        ]
    )
