from fastapi import FastAPI

from app.api.routes_appointments import router as appointments_router
from app.core.config import settings


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
    )

    @app.get("/", tags=["health"])
    def read_root():
        return {"status": "ok"}

    app.include_router(
        appointments_router,
        prefix=settings.API_V1_PREFIX + "/appointments",
        tags=["appointments"],
    )

    return app


app = create_application()



