import time
import logging
from collections import defaultdict
from typing import Dict, List
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings

logger = logging.getLogger(__name__)

# Хранилище запросов в памяти: {ip: [timestamps]}
_request_history: Dict[str, List[float]] = defaultdict(list)

# Максимум запросов в минуту на IP
RATE_LIMIT_REQUESTS = 30
RATE_LIMIT_WINDOW = 60  # секунд


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Очищаем старые записи
        _request_history[client_ip] = [
            t for t in _request_history[client_ip] if now - t < RATE_LIMIT_WINDOW
        ]

        if len(_request_history[client_ip]) >= RATE_LIMIT_REQUESTS:
            logger.warning(f"Rate limit exceeded for IP {client_ip}")
            raise HTTPException(
                status_code=429,
                detail="Слишком много запросов. Подождите и попробуйте снова.",
            )

        _request_history[client_ip].append(now)
        response = await call_next(request)
        return response