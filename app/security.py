from fastapi import HTTPException, status, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import time
from collections import deque, defaultdict

security = HTTPBearer()
API_TOKEN = os.getenv("API_TOKEN")

# Sliding window rate limiting (per IP
class RateLimiter:
    _rate_limit_storage = defaultdict(deque)
    RATE_LIMIT = 10  # requests
    RATE_PERIOD = 60  # seconds

    @classmethod
    def verify_limit(cls, request: Request):
        # Support for reverse proxy: use X-Forwarded-For if present
        xff = request.headers.get("x-forwarded-for")
        if xff:
            ip = xff.split(",")[0].strip()
        else:
            ip = getattr(request.client, "host", None)
        now = time.time()
        window_start = now - cls.RATE_PERIOD
        dq = cls._rate_limit_storage[ip]
        # Remove timestamps outside the window
        while dq and dq[0] < window_start:
            dq.popleft()
        if len(dq) >= cls.RATE_LIMIT:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        dq.append(now)
        return True

    @classmethod
    def clear_storage(cls):
        cls._rate_limit_storage = defaultdict(deque)

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")
    return True
