from uuid import UUID

from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr | None = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeOut(EmployeeBase):
    id: UUID

    class Config:
        from_attributes = True



