# Telegram-бот для перевода видео по ссылке

Бот принимает ссылку на видео, скачивает аудио, делает транскрипцию через **AssemblyAI** (официальный Python SDK из GitHub, есть бесплатный tier API), переводит текст через **LibreTranslate (self-hosted)** и отправляет пользователю пруф для подтверждения.

## Архитектура (по вашей схеме)

1. Пользователь отправляет ссылку.
2. Бот логирует ссылку в Google Sheets (опционально).
3. Бот скачивает аудио из видео (`yt-dlp` + ffmpeg).
4. Отправляет аудио в транскрибацию через официальный SDK AssemblyAI.
5. Переводит текст через локально поднятый LibreTranslate.
6. Отправляет пруф перевода с кнопками:
   - **Подтвердить** → присылает полный перевод в `.txt`, статус `approved`.
   - **Отклонить** → удаляет временный файл, статус `rejected`.

## Используемые open-source репозитории

- AssemblyAI Python SDK: https://github.com/AssemblyAI/assemblyai-python-sdk
- LibreTranslate: https://github.com/LibreTranslate/LibreTranslate

## Структура проекта

```text
bot/
  main.py                # запуск и DI зависимостей
  config.py              # env-конфиг
  handlers.py            # Telegram handlers
  keyboards.py           # inline клавиатуры
  services/
    video.py             # скачивание/чистка медиа
    transcription.py     # AssemblyAI
    translation.py       # LibreTranslate (self-hosted endpoint)
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

## Переменные окружения

Создайте `.env` в корне:

```env
TELEGRAM_BOT_TOKEN=...
ASSEMBLYAI_API_KEY=...  # ключ из личного кабинета AssemblyAI

# LibreTranslate (локальный/self-hosted)
LIBRETRANSLATE_URL=http://127.0.0.1:5000/translate
LIBRETRANSLATE_API_KEY=  # для локального LibreTranslate обычно пусто
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


## Важно про AssemblyAI

Мы действительно используем **код из GitHub** (официальный SDK `assemblyai`),
но сам SDK отправляет запросы в облачный сервис AssemblyAI.
Поэтому `ASSEMBLYAI_API_KEY` в `.env` всё равно нужен.

Если хотите полностью локальную транскрибацию без облачного ключа — нужно подключать другой движок (например, Whisper локально), это отдельная доработка.


## Важно про LibreTranslate (локально)

- Если вы подняли LibreTranslate **локально**, отдельный ключ обычно **не нужен**.
  Оставьте `LIBRETRANSLATE_API_KEY=` пустым.
- В `LIBRETRANSLATE_URL` можно указывать как `http://127.0.0.1:5000`, так и `http://127.0.0.1:5000/translate`
  (бот сам нормализует URL).

### Быстрая проверка, что локальный LibreTranslate живой

```bash
curl -X POST http://127.0.0.1:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"q":"hello","source":"en","target":"ru","format":"text"}'
```

Если в ответе есть `translatedText`, значит сервис работает корректно.

## Как поднять LibreTranslate локально (пример)

```bash
docker run -d -p 5000:5000 libretranslate/libretranslate
```

После запуска бот будет использовать `http://127.0.0.1:5000/translate` по умолчанию.

## Запуск

```bash
python -m bot.main
```

## Примечания

- Если Google Sheets не настроен, бот просто пропускает этап логирования.
- Для продакшена лучше заменить in-memory хранилище на БД (PostgreSQL/Redis).
- Для длинных видео добавьте очереди задач (Celery/RQ) и фоновую обработку.
