from dataclasses import dataclass
from enum import Enum


class JobStatus(str, Enum):
    pending_review = "pending_review"
    approved = "approved"
    rejected = "rejected"


@dataclass
class TranslationJob:
    job_id: str
    user_id: int
    source_url: str
    transcript: str
    translated_text: str
    media_path: str
    status: JobStatus = JobStatus.pending_review


class InMemoryJobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, TranslationJob] = {}

    def put(self, job: TranslationJob) -> None:
        self._jobs[job.job_id] = job

    def get(self, job_id: str) -> TranslationJob | None:
        return self._jobs.get(job_id)

    def delete(self, job_id: str) -> None:
        self._jobs.pop(job_id, None)
