from fastapi import HTTPException, status, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from collections import deque, defaultdict

from settings import settings

security = HTTPBearer()


# Sliding window rate limiting (per IP)
class RateLimiter:
    _rate_limit_storage = defaultdict(deque)

    @classmethod
    def verify_limit(cls, request: Request):
        # Support for reverse proxy: use X-Forwarded-For if present
        xff = request.headers.get("x-forwarded-for")
        if xff:
            ip = xff.split(",")[0].strip()
        else:
            ip = getattr(request.client, "host", None)
        now = time.time()
        window_start = now - settings.rate_period
        dq = cls._rate_limit_storage[ip]
        # Remove timestamps outside the window
        while dq and dq[0] < window_start:
            dq.popleft()
        if len(dq) >= settings.rate_limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        dq.append(now)
        return True

    @classmethod
    def clear_storage(cls):
        cls._rate_limit_storage = defaultdict(deque)


def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    if (
        credentials.scheme != "Bearer"
        or credentials.credentials != settings.api_token
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
        )
    return True
