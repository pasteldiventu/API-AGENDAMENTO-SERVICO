from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações principais da aplicação.
    Valores padrão são voltados para desenvolvimento.
    """

    PROJECT_NAME: str = "API de Agendamento de Serviços"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql://user:password@localhost:5432/agendamento_db"

    # Chave usada pelo Bot do WhatsApp para autenticar no endpoint de criação
    BOT_API_KEY: str = "changeme-bot-api-key"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()



