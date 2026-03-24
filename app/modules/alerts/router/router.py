from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.alerts.schemas.schemas import (
    AlertCreate,
    AlertEvaluationSummary,
    AlertRead,
    AlertUpdate,
)
from app.modules.alerts.service.service import AlertService, AlertValidationError
from app.modules.alerts.use_cases.evaluate_alerts import AlertEvaluatorUseCase

router = APIRouter(prefix="/alerts", tags=["alerts"])
service = AlertService()
evaluator_use_case = AlertEvaluatorUseCase()


@router.get("/", response_model=list[AlertRead])
async def list_alerts(
    session: AsyncSession = Depends(get_db_session),
) -> list[AlertRead]:
    return await service.list_alerts(session)


@router.post("/", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
async def create_alert(
    payload: AlertCreate,
    session: AsyncSession = Depends(get_db_session),
) -> AlertRead:
    try:
        return await service.create_alert(session, payload)
    except AlertValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "invalid_alert",
                "message": str(exc),
            },
        ) from exc


@router.post("/evaluate", response_model=AlertEvaluationSummary)
async def evaluate_alerts(
    session: AsyncSession = Depends(get_db_session),
) -> AlertEvaluationSummary:
    return await evaluator_use_case.execute(session)


@router.patch("/{alert_id}", response_model=AlertRead)
async def update_alert(
    alert_id: int,
    payload: AlertUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> AlertRead:
    try:
        alert = await service.update_alert(session, alert_id, payload)
    except AlertValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "invalid_alert_update",
                "message": str(exc),
            },
        ) from exc

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "alert_not_found",
                "message": "The requested alert does not exist.",
            },
        )

    return alert
