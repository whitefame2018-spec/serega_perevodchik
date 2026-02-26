from pathlib import Path

from bot.services.transcription import TranscriptSegment


class SubtitleService:
    @staticmethod
    def to_srt_time(seconds: float) -> str:
        total_ms = max(0, int(seconds * 1000))
        hours = total_ms // 3_600_000
        minutes = (total_ms % 3_600_000) // 60_000
        secs = (total_ms % 60_000) // 1000
        ms = total_ms % 1000
        return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"

    def write_srt(self, segments: list[TranscriptSegment], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as f:
            for idx, seg in enumerate(segments, start=1):
                start = self.to_srt_time(seg.start)
                end = self.to_srt_time(max(seg.end, seg.start + 0.3))
                f.write(f"{idx}\n{start} --> {end}\n{seg.text}\n\n")

        return output_path
