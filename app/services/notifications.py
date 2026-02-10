"""
Stubs para futuras integrações de notificação (push, webhooks para o Bot, etc.).

Por enquanto, apenas funções vazias para manter o acoplamento baixo.
"""

from uuid import UUID

from app.models.appointment import Appointment


def notify_employee_new_appointment(appointment: Appointment) -> None:
    """
    Futuro ponto de integração:
    - Enviar push notification para o app mobile
    - Disparar evento para fila, etc.
    """
    # Implementação futura
    return None


def notify_bot_on_confirmation(appointment_id: UUID) -> None:
    """
    Futuro ponto de integração:
    - Disparar webhook para o Bot avisar o cliente que o horário foi confirmado.
    """
    # Implementação futura
    return None


