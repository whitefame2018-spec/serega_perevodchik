# Telegram-бот для перевода видео по ссылке

Бот принимает ссылку на видео, скачивает видеофайл, делает транскрипцию через **Whisper (локально)**, переводит текст через **Google Translate** и отправляет пользователю **TXT-файл с готовым переводом (сценарием)**.

## Что умеет бот

1. Принимает ссылку на видео.
2. Скачивает видео (`yt-dlp`).
3. Делает локальную транскрипцию (Whisper).
4. Переводит полный текст транскрипции (Google Translate).
5. Отправляет результат в `.txt` файл в чат.

> Субтитры и отправка видео отключены: бот теперь работает только в формате «перевод -> txt».

## Структура проекта

```text
bot/
  main.py
  config.py
  handlers.py
  services/
    video.py         # скачивание видео
    transcription.py # Whisper
    translation.py   # Google Translate
    sheets.py
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

> Нужен установленный `ffmpeg` в системе (для работы с медиа).

## Переменные окружения (`.env`)

```env
TELEGRAM_BOT_TOKEN=...

# Whisper (локальная транскрибация)
WHISPER_MODEL=base
WHISPER_LANGUAGE=   # например: ru / en (пусто = автоопределение)

# Google Translate
SOURCE_LANG=auto
TARGET_LANG=ru

# Локальные файлы
TEMP_DIR=./tmp

# Опционально: Google Sheets логирование
GOOGLE_SHEETS_CREDENTIALS_PATH=./google_service_account.json
GOOGLE_SHEETS_SPREADSHEET_ID=
GOOGLE_SHEETS_WORKSHEET=Sheet1
```

## Запуск бота

```bash
python -m bot.main
```
