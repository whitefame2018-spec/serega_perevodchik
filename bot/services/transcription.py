from dataclasses import dataclass
from pathlib import Path

import whisper


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str


@dataclass
class TranscriptionResult:
    text: str
    segments: list[TranscriptSegment]


class WhisperTranscriber:
    def __init__(self, model_name: str = "base", language: str | None = None) -> None:
        self.model_name = model_name
        self.language = language
        self._model = whisper.load_model(model_name)

    def transcribe(self, media_path: Path) -> TranscriptionResult:
        result = self._model.transcribe(str(media_path), language=self.language)
        text = (result.get("text") or "").strip()
        if not text:
            raise RuntimeError("Whisper returned empty transcript")

        segments: list[TranscriptSegment] = []
        for seg in result.get("segments") or []:
            seg_text = (seg.get("text") or "").strip()
            if not seg_text:
                continue
            segments.append(
                TranscriptSegment(
                    start=float(seg.get("start", 0.0)),
                    end=float(seg.get("end", 0.0)),
                    text=seg_text,
                )
            )

        return TranscriptionResult(text=text, segments=segments)
