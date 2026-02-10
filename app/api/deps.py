from uuid import UUID

from fastapi import Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.employee import Employee


def get_bot_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """
    Valida a API Key enviada pelo Bot de WhatsApp.
    """
    if x_api_key != settings.BOT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bot API key",
        )
    return x_api_key


def get_current_employee(
    employee_id: UUID = Query(..., description="Identificador do funcionário (employee)"),
    db: Session = Depends(get_db),
) -> Employee:
    """
    Recupera o employee responsável pela requisição, usando um parâmetro simples.
    Futuramente, isto pode ser trocado para JWT.
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee



