import gzip
import logging
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth.middleware import TenantIsolationMiddleware
from app.auth.router import router as auth_router
from app.config import get_settings
from app.dependencies import close_redis
from app.routers.activity import router as activity_router
from app.routers.analytics import router as analytics_router
from app.routers.ad import router as ad_router
from app.routers.agents import router as agents_router
from app.routers.agent_ws import router as agent_ws_router  # WebSocket probe push
from app.routers.ai_report import router as ai_report_router
from app.routers.ai import router as ai_router
from app.routers.attack_paths import router as attack_paths_router
from app.routers.detection import router as detection_router
from app.routers.detection_runs import router as detection_runs_router
from app.routers.agent_advisor import router as agent_advisor_router
from app.routers.engagements import router as eng_router
from app.routers.exploits import router as exploits_router
from app.routers.findings import router as findings_router
from app.routers.health import router as health_router
from app.routers.vuln_scans import router as vuln_router

settings = get_settings()

# ── Structlog configuration ───────────────────────────────────────────────────

shared_processors = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
]

if settings.is_production:
    structlog.configure(
        processors=[*shared_processors, structlog.processors.JSONRenderer()],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.PrintLoggerFactory(),
    )
else:
    structlog.configure(
        processors=[*shared_processors, structlog.dev.ConsoleRenderer()],
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
        logger_factory=structlog.PrintLoggerFactory(),
    )

logger = structlog.get_logger()


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("vedha_api.startup", env=settings.app_env)
    yield
    logger.info("vedha_api.shutdown")
    await close_redis()


# ── App factory ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="Vedha VAPT Platform API",
    description=(
        "Backend for the Vedha automated Network VAPT platform. "
        "Handles multi-tenant engagements, asset management, finding triage, "
        "attack path analysis, and detection coverage."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# ── gzip request decoding ─────────────────────────────────────────────────────
# Probes gzip large scan-result payloads (a /24 sweep is MBs of JSON). Starlette
# decodes Content-Encoding on *responses* but not *requests*, so without this a
# gzipped body reaches the route as raw compressed bytes and JSON parsing 400s.
# We buffer + inflate only when the client advertises `Content-Encoding: gzip`;
# every other request is passed through untouched (zero overhead).
class GzipRequestMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = dict(scope.get("headers") or [])
        if b"gzip" not in headers.get(b"content-encoding", b"").lower():
            return await self.app(scope, receive, send)

        # Buffer the full (compressed) body.
        chunks: list[bytes] = []
        while True:
            msg = await receive()
            if msg["type"] == "http.request":
                chunks.append(msg.get("body", b""))
                if not msg.get("more_body", False):
                    break
            elif msg["type"] == "http.disconnect":
                break
        try:
            body = gzip.decompress(b"".join(chunks))
        except (OSError, EOFError):
            # Not valid gzip — reject cleanly rather than corrupting the route.
            return await JSONResponse(
                {"detail": "malformed gzip request body"}, status_code=400,
            )(scope, receive, send)

        # Rewrite headers: drop content-encoding, fix content-length.
        new_headers = [
            (k, v) for (k, v) in scope["headers"]
            if k not in (b"content-encoding", b"content-length")
        ]
        new_headers.append((b"content-length", str(len(body)).encode()))
        scope = {**scope, "headers": new_headers}

        delivered = False

        async def receive_inflated():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": body, "more_body": False}
            return {"type": "http.disconnect"}

        return await self.app(scope, receive_inflated, send)


# ── Middleware (order matters: outermost first) ───────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TenantIsolationMiddleware)
app.add_middleware(GzipRequestMiddleware)


# ── Global exception handlers ─────────────────────────────────────────────────

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error("unhandled_exception", path=request.url.path, exc=str(exc), exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


# ── Routers ───────────────────────────────────────────────────────────────────

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(eng_router)
app.include_router(findings_router)
app.include_router(agents_router)
app.include_router(agent_ws_router)
app.include_router(vuln_router)
app.include_router(exploits_router)
app.include_router(ad_router)
app.include_router(attack_paths_router)
app.include_router(detection_router)
app.include_router(detection_runs_router)
app.include_router(agent_advisor_router)
app.include_router(ai_report_router)
app.include_router(ai_router)
app.include_router(activity_router)
app.include_router(analytics_router)


# ── P2: Prometheus metrics — request latency/count/in-progress at /metrics, so
# the bottleneck (result-submit + findings paths) is measurable under load, not
# guessed. Scrape with Prometheus; the data drives the P3 scaling decisions. ──
try:
    from prometheus_fastapi_instrumentator import Instrumentator
    Instrumentator(excluded_handlers=["/metrics", "/health"]).instrument(app).expose(
        app, endpoint="/metrics", include_in_schema=False)
except Exception as _exc:  # noqa: BLE001 — metrics must never block startup
    structlog.get_logger().warning("metrics.init_failed", error=str(_exc))


@app.get("/", include_in_schema=False)
async def _service_root():
    """Identify the Manager API without exposing a second dashboard."""
    return {
        "service": "Vedha Manager API",
        "status": "ok",
        "dashboard": "Use the Vedha Next.js dashboard.",
        "docs": "/docs",
    }
