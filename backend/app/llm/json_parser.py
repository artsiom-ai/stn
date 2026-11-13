import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def parse_json_with_retry(raw: str, max_retries: int = 2) -> Optional[Dict[str, Any]]:
    """
    Попытка распарсить JSON из строки.
    Если не получается — пытаемся извлечь JSON-блок из markdown-обёртки,
    делаем до max_retries попыток (передаём модель raw снова, но здесь
    возвращаем None, чтобы вызывающий код решил, делать ли ретрай запроса).
    """
    if not raw or not raw.strip():
        return None

    text = raw.strip()

    # Убираем markdown-обёртки вида ```json ... ```
    if "```" in text:
        start = text.find("```")
        end = text.rfind("```")
        if end > start:
            block = text[start + 3:end]
            # Убираем возможную метку языка
            if block.startswith("json"):
                block = block[4:]
            text = block.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse error: {e}. Raw: {text[:200]}...")
        return None


def extract_json_block(text: str) -> Optional[str]:
    """Пытается выделить блок JSON из текста, обёрнутого в ```json ... ```."""
    if not text:
        return None
    if "```" in text:
        start = text.find("```")
        end = text.rfind("```")
        if end > start:
            block = text[start + 3:end]
            if block.startswith("json"):
                block = block[4:]
            return block.strip()
    return text.strip()