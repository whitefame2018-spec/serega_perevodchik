from pathlib import Path

import whisper


class WhisperTranscriber:
    def __init__(self, model_name: str = "base", language: str | None = None) -> None:
        self.model_name = model_name
        self.language = language
        self._model = whisper.load_model(model_name)

    def transcribe(self, media_path: Path) -> str:
        result = self._model.transcribe(str(media_path), language=self.language)
        text = (result.get("text") or "").strip()
        if not text:
            raise RuntimeError("Whisper returned empty transcript")
        return text
