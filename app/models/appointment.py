from datetime import date, datetime, time, timezone
from uuid import uuid4

from sqlalchemy import Date, ForeignKey, String, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    client_name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_phone: Mapped[str] = mapped_column(String(32), nullable=False)
    service_type: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Campos separados de data e hora solicitadas (UTC)
    request_date: Mapped[date] = mapped_column(Date, nullable=False)
    request_time: Mapped[time] = mapped_column(Time, nullable=False)

    # Status armazenado como string simples
    status: Mapped[str] = mapped_column(String(64), nullable=False, default="PENDING_APPROVAL")

    notes: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    employee_id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )

    employee = relationship("Employee", backref="appointments")

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    @property
    def requested_at(self) -> datetime:
        """
        Helper para combinar request_date + request_time em um datetime (UTC).
        Útil para ordenação e cálculos de meta_ui.
        """
        return datetime.combine(self.request_date, self.request_time).replace(tzinfo=timezone.utc)



