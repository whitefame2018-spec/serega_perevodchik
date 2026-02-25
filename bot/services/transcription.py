from pathlib import Path

import assemblyai as aai


class AssemblyAITranscriber:
    def __init__(self, api_key: str) -> None:
        aai.settings.api_key = api_key
        self._transcriber = aai.Transcriber()

    def transcribe(self, media_path: Path) -> str:
        transcript = self._transcriber.transcribe(str(media_path))

        if transcript.status == aai.TranscriptStatus.error:
            raise RuntimeError(transcript.error or "Transcription failed")
        if not transcript.text:
            raise RuntimeError("AssemblyAI returned empty transcript")

        return transcript.text
