from datetime import date, time, datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field


class MetaUI(BaseModel):
    is_today: bool
    urgency_level: str
    display_time: str
    relative_time: str


class AppointmentBase(BaseModel):
    client_name: str
    client_phone: str
    service_type: str | None = None
    request_date: date
    request_time: time
    notes: str | None = None


class AppointmentCreate(AppointmentBase):
    # Nome lógico interno employee_id, mas pode aceitar alias collaborator_id
    employee_id: UUID = Field(..., alias="employee_id")

    class Config:
        populate_by_name = True


class AppointmentOut(AppointmentBase):
    id: UUID
    status: str
    employee_id: UUID
    created_at: datetime
    updated_at: datetime
    meta_ui: MetaUI | None = None

    class Config:
        from_attributes = True

    @staticmethod
    def build_meta_ui(request_date: date, request_time: time) -> MetaUI:
        """
        Constrói meta_ui simples, alinhado com a ideia da documentação:
        - is_today
        - urgency_level (high/normal/low)
        - display_time (HH:MM)
        - relative_time (texto amigável e aproximado)
        """
        now = datetime.now(timezone.utc)
        requested_at = datetime.combine(request_date, request_time).replace(tzinfo=timezone.utc)

        is_today = requested_at.date() == now.date()

        delta = requested_at - now
        total_minutes = int(delta.total_seconds() // 60)

        if total_minutes < 0:
            urgency = "past"
        elif total_minutes <= 120:
            urgency = "high"
        elif is_today:
            urgency = "normal"
        else:
            urgency = "low"

        if total_minutes < 0:
            relative = "já ocorreu"
        elif total_minutes < 60:
            relative = f"em {total_minutes} minutos"
        elif total_minutes < 24 * 60:
            hours = total_minutes // 60
            relative = f"em {hours} horas"
        elif total_minutes < 48 * 60:
            relative = "amanhã"
        else:
            days = total_minutes // (24 * 60)
            relative = f"em {days} dias"

        return MetaUI(
            is_today=is_today,
            urgency_level=urgency,
            display_time=request_time.strftime("%H:%M"),
            relative_time=relative,
        )


