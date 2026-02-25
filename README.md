# Telegram-бот для перевода видео по ссылке

Бот принимает ссылку на видео, скачивает аудио, делает транскрипцию через **AssemblyAI** (есть бесплатный tier), переводит текст через **LibreTranslate API** и отправляет пользователю пруф для подтверждения.

## Архитектура (по вашей схеме)

1. Пользователь отправляет ссылку.
2. Бот логирует ссылку в Google Sheets (опционально).
3. Бот скачивает аудио из видео (`yt-dlp` + ffmpeg).
4. Отправляет аудио в транскрибацию (AssemblyAI).
5. Переводит текст (LibreTranslate).
6. Отправляет пруф перевода с кнопками:
   - **Подтвердить** → присылает полный перевод в `.txt`, статус `approved`.
   - **Отклонить** → удаляет временный файл, статус `rejected`.

## Структура проекта

```text
bot/
  main.py                # запуск и DI зависимостей
  config.py              # env-конфиг
  handlers.py            # Telegram handlers
  keyboards.py           # inline клавиатуры
  services/
    video.py             # скачивание/чистка медиа
    transcription.py     # AssemblyAI API
    translation.py       # LibreTranslate API
    sheets.py            # Google Sheets логирование
    storage.py           # in-memory хранилище задач
requirements.txt
```

## Установка

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Windows (cmd)

```bat
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

> Нужен установленный `ffmpeg` в системе (на Windows удобно поставить через `winget install Gyan.FFmpeg` или `choco install ffmpeg`).
> Нужен установленный `ffmpeg` в системе.

## Переменные окружения

Создайте `.env` в корне:

```env
TELEGRAM_BOT_TOKEN=...
ASSEMBLYAI_API_KEY=...

# LibreTranslate
LIBRETRANSLATE_URL=https://libretranslate.com/translate
LIBRETRANSLATE_API_KEY=
SOURCE_LANG=auto
TARGET_LANG=ru

# Локальные временные файлы
TEMP_DIR=./tmp
MAX_PREVIEW_CHARS=1400

# Опционально: Google Sheets логирование
GOOGLE_SHEETS_CREDENTIALS_PATH=./google_service_account.json
GOOGLE_SHEETS_SPREADSHEET_ID=
GOOGLE_SHEETS_WORKSHEET=Sheet1
```

## Запуск

```bash
python -m bot.main
```

## Примечания

- Если Google Sheets не настроен, бот просто пропускает этап логирования.
- Для продакшена лучше заменить in-memory хранилище на БД (PostgreSQL/Redis).
- Для длинных видео добавьте очереди задач (Celery/RQ) и фоновую обработку.
