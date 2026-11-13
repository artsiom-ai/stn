import json
import logging
from typing import Any, Dict, Optional

from app.config import settings
from app.llm.base import LLMProvider
from app.llm.json_parser import parse_json_with_retry
from app.llm.openai import OpenAIProvider
from app.llm.anthropic import AnthropicProvider

logger = logging.getLogger(__name__)


class LLMRouter:
    """
    Роутер LLM с фолбэком между провайдерами и ретраями при битом JSON.
    Никогда не логирует API-ключи.
    """

    def __init__(self):
        self.providers: list[LLMProvider] = []
        self._build_providers()

    def _build_providers(self):
        primary = settings.LLM_PROVIDER_PRIMARY
        fallback = settings.LLM_PROVIDER_FALLBACK

        provider_classes = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
        }

        order = [p for p in [primary, fallback] if p in provider_classes]
        # Добавляем剩余 providers, чтобы не потерять ни одного
        for name in provider_classes:
            if name not in order:
                order.append(name)

        for name in order:
            try:
                provider = provider_classes[name]()
                self.providers.append(provider)
                logger.info(f"LLM provider registered: {name}")
            except Exception as e:
                logger.warning(f"Failed to register LLM provider '{name}': {e}")

    async def complete(self, prompt: str, system_prompt: Optional[str] = None,
                       temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Выполнить запрос с фолбэком между провайдерами."""
        last_error = None
        for provider in self.providers:
            try:
                return await provider.complete(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            except Exception as e:
                last_error = e
                logger.warning(f"LLM provider failed: {type(e).__name__}, trying next")
        raise RuntimeError(f"All LLM providers failed. Last error: {last_error}")

    async def complete_json(self, prompt: str, system_prompt: Optional[str] = None,
                            temperature: float = 0.3, max_tokens: int = 1000,
                            max_retries: int = 2) -> Dict[str, Any]:
        """
        Выполнить запрос и распарсить ответ как JSON.
        При битом JSON делает до max_retries повторных запросов к тому же или
        следующему провайдеру. Если всё ещё бито — возвращает понятную ошибку.
        """
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                raw = await self.complete(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                parsed = parse_json_with_retry(raw)
                if parsed is not None:
                    return parsed
                last_error = "Invalid JSON from LLM"
                logger.warning(f"Invalid JSON on attempt {attempt + 1}")
            except Exception as e:
                last_error = str(e)
                logger.warning(f"LLM error on attempt {attempt + 1}: {type(e).__name__}")

        raise ValueError(
            "Не удалось получить корректный JSON от LLM после нескольких попыток. "
            "Попробуйте позже или обратитесь к наставнику."
        )