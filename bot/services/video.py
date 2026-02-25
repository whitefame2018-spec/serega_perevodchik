from pathlib import Path

import yt_dlp


class VideoService:
    def __init__(self, temp_dir: str) -> None:
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def download_audio(self, url: str, job_id: str) -> Path:
        output_template = str(self.temp_dir / f"{job_id}.%(ext)s")
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "quiet": True,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        result = self.temp_dir / f"{job_id}.mp3"
        if not result.exists():
            raise FileNotFoundError(f"Audio file not found for job {job_id}")
        return result

    def cleanup(self, media_path: str) -> None:
        path = Path(media_path)
        if path.exists():
            path.unlink()
