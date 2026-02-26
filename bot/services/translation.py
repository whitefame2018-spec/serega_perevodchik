from urllib.parse import urlparse

import httpx


class LibreTranslator:
    def __init__(
        self,
        base_url: str,
        source_lang: str,
        target_lang: str,
        api_key: str | None = None,
    ) -> None:
        self.base_url = self._normalize_url(base_url)
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.api_key = api_key

    @staticmethod
    def _normalize_url(base_url: str) -> str:
        url = base_url.strip().rstrip("/")
        path = urlparse(url).path
        if path in {"", "/"}:
            return f"{url}/translate"
        return url

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
            response = client.post(
                self.base_url,
                json=payload,
                headers={"accept": "application/json"},
            )
            if response.status_code >= 400:
                raise RuntimeError(
                    f"LibreTranslate request failed ({response.status_code}): {response.text}"
                )

            data = response.json()
            translated = data.get("translatedText")
            if not translated:
                raise RuntimeError(f"LibreTranslate returned unexpected payload: {data}")

            return translated
