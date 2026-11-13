import logging
from typing import Optional

from app.config import settings
from app.llm.base import LLMProvider

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from anthropic import AsyncAnthropic
                self._client = AsyncAnthropic(api_key=self.api_key)
            except ImportError:
                logger.error("anthropic package not installed")
                raise
        return self._client

    async def complete(self, prompt: str, system_prompt: Optional[str] = None,
                       temperature: float = 0.7, max_tokens: int = 1000) -> str:
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not configured")
        client = self._get_client()
        kwargs = dict(
            model="claude-3-haiku-20240307",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if system_prompt:
            kwargs["system"] = system_prompt
        response = await client.messages.create(**kwargs)
        return response.content[0].text if response.content else ""

    def mask_key(self, key: str) -> str:
        if not key:
            return "empty"
        return f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "***"