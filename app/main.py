import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.error_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.jobs.alert_evaluator import AlertEvaluatorJob

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    stop_event = asyncio.Event()
    app.state.alert_job_stop_event = stop_event
    app.state.alert_job_task = None

    if not getattr(app.state, "disable_scheduler", False):
        job = AlertEvaluatorJob(
            interval_seconds=settings.alert_evaluation_interval_seconds,
        )
        task = asyncio.create_task(job.run_forever(stop_event))
        app.state.alert_job_task = task
        logger.info(
            "Alert evaluator scheduler started with interval_seconds=%s",
            settings.alert_evaluation_interval_seconds,
        )
    else:
        logger.info("Alert evaluator scheduler disabled for this application instance.")

    try:
        yield
    finally:
        stop_event.set()
        task = getattr(app.state, "alert_job_task", None)
        if task is not None:
            await task
            logger.info("Alert evaluator scheduler stopped.")


app = FastAPI(
    title=settings.project_name,
    lifespan=lifespan,
)
register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_prefix)
