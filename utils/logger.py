import json
import time
from datetime import datetime, timezone
from urllib.parse import urlencode, parse_qsl

MAX_BODY_CHARS = 500


def _client_ip(scope) -> str:
    headers = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope.get("headers", [])}
    forwarded = headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    client = scope.get("client")
    if client:
        return client[0]
    return "-"


def _format_params(query_string: bytes) -> str:
    if not query_string:
        return "-"
    pairs = [(k, "***" if k == "api_key" else v)
             for k, v in parse_qsl(query_string.decode("latin-1"), keep_blank_values=True)]
    return urlencode(pairs, safe="*")


def _format_body(body: bytes) -> str:
    if not body:
        return "-"
    text = body.decode("utf-8", errors="replace")
    try:
        text = json.dumps(json.loads(text), separators=(",", ":"), default=str)
    except (ValueError, TypeError):
        pass
    text = " ".join(text.split())
    if len(text) > MAX_BODY_CHARS:
        text = text[: MAX_BODY_CHARS - 3] + "..."
    return text


class RequestLoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        body = b""
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                break
            body += message.get("body", b"")
            if not message.get("more_body", False):
                break

        async def replay_receive():
            return {"type": "http.request", "body": body, "more_body": False}

        status_code = 0
        started = time.perf_counter()

        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            await self.app(scope, replay_receive, send_wrapper)
        except Exception:
            self._emit(scope, body, status_code or 500, started)
            raise
        self._emit(scope, body, status_code or 500, started)

    def _emit(self, scope, body: bytes, status_code: int, started: float) -> None:
        latency_ms = int((time.perf_counter() - started) * 1000)
        query = scope.get("query_string", b"")
        api_key = "-"
        for key, value in parse_qsl(query.decode("latin-1"), keep_blank_values=True):
            if key == "api_key":
                api_key = value
                break
        timestamp = (datetime.now(timezone.utc)
                     .isoformat(timespec="milliseconds")
                     .replace("+00:00", "Z"))
        print(
            f"{timestamp} | {scope.get('method', '-')} | {status_code} | {latency_ms}ms | "
            f"{api_key} | {_client_ip(scope)} | {scope.get('path', '-')} | "
            f"{_format_params(query)} | {_format_body(body)}",
            flush=True,
        )
