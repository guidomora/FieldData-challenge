import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.database import SessionFactory
from app.modules.alerts.schemas.schemas import AlertEvaluationSummary
from app.modules.alerts.use_cases.evaluate_alerts import AlertEvaluatorUseCase

logger = logging.getLogger(__name__)


class AlertEvaluatorJob:
    def __init__(
        self,
        *,
        use_case: AlertEvaluatorUseCase | None = None,
        session_factory: async_sessionmaker[AsyncSession] | None = None,
        interval_seconds: int = 60,
    ) -> None:
        self.use_case = use_case or AlertEvaluatorUseCase()
        self.session_factory = session_factory or SessionFactory
        self.interval_seconds = interval_seconds

    async def run_once(self) -> AlertEvaluationSummary:
        logger.info("Running alert evaluator job iteration.")
        async with self.session_factory() as session:
            result = await self.use_case.execute(session)
            logger.info(
                "Alert evaluator job iteration finished processed_alerts=%s notifications_created=%s",
                result.processed_alerts,
                result.notifications_created,
            )
            return result

    async def run_forever(self, stop_event: asyncio.Event) -> None:
        logger.info(
            "Alert evaluator job loop started interval_seconds=%s",
            self.interval_seconds,
        )
        while not stop_event.is_set():
            try:
                await self.run_once()
            except Exception:
                logger.exception("Alert evaluator job failed during execution.")

            try:
                await asyncio.wait_for(stop_event.wait(), timeout=self.interval_seconds)
            except asyncio.TimeoutError:
                continue
        logger.info("Alert evaluator job loop stopped.")
