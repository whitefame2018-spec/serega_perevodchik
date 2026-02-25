import httpx


class LibreTranslator:
    def __init__(
        self,
        base_url: str,
        source_lang: str,
        target_lang: str,
        api_key: str | None = None,
    ) -> None:
        self.base_url = base_url
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.api_key = api_key

    def translate(self, text: str) -> str:
        payload = {
            "q": text,
            "source": self.source_lang,
            "target": self.target_lang,
            "format": "text",
        }
        if self.api_key:
            payload["api_key"] = self.api_key

        with httpx.Client(timeout=90.0) as client:
            response = client.post(self.base_url, data=payload)
            response.raise_for_status()
            return response.json()["translatedText"]
