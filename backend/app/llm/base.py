from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Базовый интерфейс провайдера LLM."""

    @abstractmethod
    async def complete(self, prompt: str, system_prompt: Optional[str] = None,
                       temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Выполнить запрос к модели и вернуть текст ответа."""
        pass

    @abstractmethod
    def mask_key(self, key: str) -> str:
        """Замаскировать ключ для безопасного логирования."""
        pass