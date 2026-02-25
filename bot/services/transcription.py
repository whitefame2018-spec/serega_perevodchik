import time
from pathlib import Path

import httpx


class AssemblyAITranscriber:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://api.assemblyai.com/v2"

    @property
    def _headers(self) -> dict[str, str]:
        return {"authorization": self.api_key}

    def transcribe(self, media_path: Path) -> str:
        upload_url = self._upload_file(media_path)
        transcript_id = self._request_transcription(upload_url)
        return self._poll_result(transcript_id)

    def _upload_file(self, media_path: Path) -> str:
        with media_path.open("rb") as f, httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{self.base_url}/upload",
                headers=self._headers,
                content=f,
            )
            response.raise_for_status()
            return response.json()["upload_url"]

    def _request_transcription(self, upload_url: str) -> str:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{self.base_url}/transcript",
                headers={**self._headers, "content-type": "application/json"},
                json={"audio_url": upload_url},
            )
            response.raise_for_status()
            return response.json()["id"]

    def _poll_result(self, transcript_id: str) -> str:
        with httpx.Client(timeout=30.0) as client:
            while True:
                response = client.get(
                    f"{self.base_url}/transcript/{transcript_id}",
                    headers=self._headers,
                )
                response.raise_for_status()
                payload = response.json()
                status = payload.get("status")

                if status == "completed":
                    return payload["text"]
                if status == "error":
                    raise RuntimeError(payload.get("error", "Transcription failed"))

                time.sleep(3)
