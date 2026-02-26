# Telegram-бот для перевода видео по ссылке

Бот принимает ссылку на видео, скачивает видеофайл, делает транскрипцию через **Whisper (локально)**, переводит сегменты через **LibreTranslate (self-hosted)** и отправляет пользователю **видео с переведёнными субтитрами** + текст перевода.

## Что умеет бот

1. Принимает ссылку на видео.
2. Скачивает видео (`yt-dlp`).
3. Делает локальную транскрипцию (Whisper).
4. Переводит сегменты транскрипции (LibreTranslate).
5. Генерирует `.srt` и вшивает субтитры в видео (`ffmpeg`).
6. Отправляет пруф, затем по approve присылает `.txt` + видео с переводом.

> Сейчас реализован вариант **субтитров**. Архитектура позволяет позже добавить озвучку (TTS + микширование аудио), если потребуется.

## Структура проекта

```text
bot/
  main.py
  config.py
  handlers.py
  keyboards.py
  services/
    video.py         # скачивание видео + вшивание субтитров
    transcription.py # Whisper + сегменты
    translation.py   # LibreTranslate
    subtitles.py     # генерация .srt
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

## Проверка LibreTranslate (локально)

```bash
curl -X POST http://127.0.0.1:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"q":"hello","source":"en","target":"ru","format":"text"}'
```

## Как поднять LibreTranslate локально

```bash
docker run -d -p 5000:5000 libretranslate/libretranslate
```

## Запуск бота

```bash
python -m bot.main
```
