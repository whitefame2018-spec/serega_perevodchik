# Telegram-бот для перевода видео по ссылке

Бот принимает ссылку на видео, скачивает аудио, делает транскрипцию через **Whisper (локально)**, переводит текст через **LibreTranslate (self-hosted)** и отправляет пользователю пруф для подтверждения.

## Архитектура

1. Пользователь отправляет ссылку.
2. Бот (опционально) логирует ссылку в Google Sheets.
3. Бот скачивает аудио (`yt-dlp` + ffmpeg).
4. Делает локальную транскрибацию через Whisper.
5. Переводит текст через локальный LibreTranslate.
6. Отправляет пруф с кнопками approve/reject.

## Структура проекта

```text
bot/
  main.py
  config.py
  handlers.py
  keyboards.py
  services/
    video.py
    transcription.py  # Whisper
    translation.py    # LibreTranslate
    sheets.py
    storage.py
requirements.txt
```

## Установка

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Windows (cmd)

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

> Нужен установленный `ffmpeg` в системе.

## Частая ошибка: `ModuleNotFoundError: No module named aiogram`

Зависимости установлены не в тот Python/окружение.

Проверьте:

```bash
python -m pip show aiogram
python -c "import aiogram; print(aiogram.__version__)"
```

## Переменные окружения (`.env`)

```env
TELEGRAM_BOT_TOKEN=...

# Whisper (локальная транскрибация)
WHISPER_MODEL=base
WHISPER_LANGUAGE=   # например: ru / en (пусто = автоопределение)

# LibreTranslate (локальный/self-hosted)
LIBRETRANSLATE_URL=http://127.0.0.1:5000/translate
LIBRETRANSLATE_API_KEY=  # обычно пусто для локального запуска
SOURCE_LANG=auto
TARGET_LANG=ru

# Локальные файлы
TEMP_DIR=./tmp
MAX_PREVIEW_CHARS=1400

# Опционально: Google Sheets логирование
GOOGLE_SHEETS_CREDENTIALS_PATH=./google_service_account.json
GOOGLE_SHEETS_SPREADSHEET_ID=
GOOGLE_SHEETS_WORKSHEET=Sheet1
```

## Как поднять LibreTranslate локально

```bash
docker run -d -p 5000:5000 libretranslate/libretranslate
```

## Запуск бота

```bash
python -m bot.main
```

## Важно про Whisper

- Whisper работает **локально**, ключ API для транскрибации не нужен.
- Первый запуск может быть дольше, потому что загружается модель.
- Можно менять размер модели через `WHISPER_MODEL` (`tiny`, `base`, `small`, `medium`, `large`).
