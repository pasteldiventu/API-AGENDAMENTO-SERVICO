from datetime import date
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.api.deps import get_bot_api_key, get_current_employee
from app.db.session import get_db
from app.models.appointment import Appointment
from app.models.employee import Employee
from app.schemas.appointment import AppointmentCreate, AppointmentOut

router = APIRouter()


@router.post(
    "/",
    response_model=AppointmentOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_bot_api_key)],
)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
) -> AppointmentOut:
    """
    Endpoint chamado pelo Bot de WhatsApp para criar um novo agendamento.
    Protegido por X-API-Key.
    """
    employee: Employee | None = (
        db.query(Employee).filter(Employee.id == payload.employee_id).first()
    )
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found for provided employee_id",
        )

    appointment = Appointment(
        client_name=payload.client_name,
        client_phone=payload.client_phone,
        service_type=payload.service_type,
        request_date=payload.request_date,
        request_time=payload.request_time,
        status="PENDING_APPROVAL",
        notes=payload.notes,
        employee_id=payload.employee_id,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    out = AppointmentOut.model_validate(appointment)
    out.meta_ui = AppointmentOut.build_meta_ui(
        request_date=appointment.request_date,
        request_time=appointment.request_time,
    )
    return out


@router.get(
    "/my-agenda",
    response_model=List[AppointmentOut],
)
def get_my_agenda(
    current_employee: Employee = Depends(get_current_employee),
    db: Session = Depends(get_db),
    status_filter: Optional[str] = Query(
        None,
        description="Filtrar por status (ex: PENDING_APPROVAL,CONFIRMED). Se vazio, retorna pendentes e confirmados.",
    ),
    from_date: Optional[date] = Query(
        None,
        description="Data inicial (UTC). Se omitida, assume hoje.",
    ),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[AppointmentOut]:
    """
    Retorna lista de agendamentos do employee logado (simplificado).
    Ordenado por request_date ASC, request_time ASC.
    """
    q = db.query(Appointment).filter(Appointment.employee_id == current_employee.id)

    # Filtro de data
    if from_date:
        q = q.filter(Appointment.request_date >= from_date)
    else:
        today = date.today()
        q = q.filter(Appointment.request_date >= today)

    # Filtro de status
    if status_filter:
        statuses = [s.strip() for s in status_filter.split(",") if s.strip()]
    else:
        statuses = ["PENDING_APPROVAL", "CONFIRMED"]

    if statuses:
        q = q.filter(Appointment.status.in_(statuses))

    q = q.order_by(
        asc(Appointment.request_date),
        asc(Appointment.request_time),
    ).offset(offset).limit(limit)

    appointments = q.all()

    results: list[AppointmentOut] = []
    for appt in appointments:
        item = AppointmentOut.model_validate(appt)
        item.meta_ui = AppointmentOut.build_meta_ui(
            request_date=appt.request_date,
            request_time=appt.request_time,
        )
        results.append(item)

    return results


@router.patch(
    "/{appointment_id}/confirm",
    response_model=AppointmentOut,
)
def confirm_appointment(
    appointment_id: UUID,
    current_employee: Employee = Depends(get_current_employee),
    db: Session = Depends(get_db),
) -> AppointmentOut:
    """
    Confirma um agendamento (de PENDING_APPROVAL para CONFIRMED).
    """
    appointment: Appointment | None = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id,
            Appointment.employee_id == current_employee.id,
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    if appointment.status == "CANCELLED":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot confirm a cancelled appointment",
        )

    if appointment.status == "CONFIRMED":
        # Idempotente: apenas retorna o recurso
        out = AppointmentOut.model_validate(appointment)
        out.meta_ui = AppointmentOut.build_meta_ui(
            request_date=appointment.request_date,
            request_time=appointment.request_time,
        )
        return out

    appointment.status = "CONFIRMED"
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    out = AppointmentOut.model_validate(appointment)
    out.meta_ui = AppointmentOut.build_meta_ui(
        request_date=appointment.request_date,
        request_time=appointment.request_time,
    )
    return out


@router.patch(
    "/{appointment_id}/cancel",
    response_model=AppointmentOut,
)
def cancel_appointment(
    appointment_id: UUID,
    current_employee: Employee = Depends(get_current_employee),
    db: Session = Depends(get_db),
    reason: Optional[str] = Query(
        None,
        description="Motivo do cancelamento (será salvo em notes).",
    ),
) -> AppointmentOut:
    """
    Cancela um agendamento (por imprevisto).
    """
    appointment: Appointment | None = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id,
            Appointment.employee_id == current_employee.id,
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    appointment.status = "CANCELLED"
    if reason:
        appointment.notes = (appointment.notes or "") + f"\n[CANCEL]: {reason}"

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    out = AppointmentOut.model_validate(appointment)
    out.meta_ui = AppointmentOut.build_meta_ui(
        request_date=appointment.request_date,
        request_time=appointment.request_time,
    )
    return out


