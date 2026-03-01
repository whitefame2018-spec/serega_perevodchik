from deep_translator import GoogleTranslator

from bot.services.transcription import TranscriptSegment


class GoogleTranslateService:
    def __init__(self, source_lang: str, target_lang: str) -> None:
        self.source_lang = source_lang
        self.target_lang = target_lang

    def translate(self, text: str) -> str:
        clean_text = text.strip()
        if not clean_text:
            return ""

        try:
            return GoogleTranslator(source=self.source_lang, target=self.target_lang).translate(clean_text)
        except Exception as exc:
            raise RuntimeError(f"Google Translate request failed: {exc}") from exc

    def translate_segments(self, segments: list[TranscriptSegment]) -> list[TranscriptSegment]:
        translated_segments: list[TranscriptSegment] = []
        for segment in segments:
            translated_segments.append(
                TranscriptSegment(
                    start=segment.start,
                    end=segment.end,
                    text=self.translate(segment.text),
                )
            )
        return translated_segments
