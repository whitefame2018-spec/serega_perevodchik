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

    def burn_subtitles(self, input_video: Path, subtitles_file: Path, job_id: str) -> Path:
        output_video = self.temp_dir / f"{job_id}_subtitled.mp4"
        escaped_subtitles = str(subtitles_file).replace("\\", "\\\\").replace(":", "\\:")

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_video),
            "-vf",
            f"subtitles={escaped_subtitles}",
            "-c:a",
            "copy",
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
