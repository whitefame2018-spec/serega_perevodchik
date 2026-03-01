from pathlib import Path
import subprocess

import yt_dlp


class VideoService:
    def __init__(self, temp_dir: str) -> None:
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def download_video(self, url: str, job_id: str) -> Path:
        output_template = str(self.temp_dir / f"{job_id}.%(ext)s")
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": output_template,
            "quiet": True,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        result = self.temp_dir / f"{job_id}.mp4"
        if not result.exists():
            raise FileNotFoundError(f"Video file not found for job {job_id}")
        return result

    @staticmethod
    def _format_subtitles_path_for_ffmpeg(subtitles_file: Path) -> str:
        normalized = subtitles_file.resolve().as_posix()
        escaped = normalized.replace("'", r"'\\''")
        escaped = escaped.replace(":", r"\:")
        return f"'{escaped}'"

    def burn_subtitles(self, input_video: Path, subtitles_file: Path, job_id: str) -> Path:
        output_video = self.temp_dir / f"{job_id}_subtitled.mp4"
        subtitles_arg = self._format_subtitles_path_for_ffmpeg(subtitles_file)

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_video),
            "-vf",
            f"subtitles={subtitles_arg}",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "28",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            str(output_video),
        ]
        process = subprocess.run(cmd, capture_output=True, text=True)
        if process.returncode != 0:
            raise RuntimeError(f"ffmpeg subtitles burn failed: {process.stderr}")

        return output_video

    def cleanup(self, media_path: str) -> None:
        path = Path(media_path)
        if path.exists():
            path.unlink()
