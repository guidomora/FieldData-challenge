import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.jobs.alert_evaluator import AlertEvaluatorJob
from app.modules.alerts.schemas.schemas import AlertEvaluationSummary


class DummySessionContextManager:
    def __init__(self, session) -> None:
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        return False


class DummySessionFactory:
    def __init__(self, session) -> None:
        self.session = session

    def __call__(self):
        return DummySessionContextManager(self.session)


@pytest.mark.asyncio
async def test_given_job_when_running_once_then_it_invokes_use_case_with_session():
    session = SimpleNamespace(name="session")
    expected_result = AlertEvaluationSummary(processed_alerts=1, notifications_created=0)
    use_case = SimpleNamespace(execute=AsyncMock(return_value=expected_result))
    job = AlertEvaluatorJob(
        use_case=use_case,
        session_factory=DummySessionFactory(session),
        interval_seconds=60,
    )

    result = await job.run_once()

    use_case.execute.assert_awaited_once_with(session)
    assert result == expected_result


@pytest.mark.asyncio
async def test_given_running_job_when_stop_event_is_set_then_loop_stops_after_single_iteration():
    session = SimpleNamespace(name="session")
    stop_event = asyncio.Event()
    use_case = SimpleNamespace(execute=AsyncMock(side_effect=lambda _: stop_event.set()))
    job = AlertEvaluatorJob(
        use_case=use_case,
        session_factory=DummySessionFactory(session),
        interval_seconds=60,
    )

    await job.run_forever(stop_event)

    use_case.execute.assert_awaited_once_with(session)
