## API de Agendamento de Serviços (FastAPI)

Backend para um sistema de agendamento de serviços integrado a um Bot de WhatsApp e a um app mobile de colaboradores (employees).

### Tecnologias

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy 2.x**

### Configuração

1. Crie e configure o banco PostgreSQL.
2. Crie um arquivo `.env` na raiz:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/agendamento_db
BOT_API_KEY=changeme-bot-api-key
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Inicialize o banco:

```bash
python -m app.init_db
```

5. Suba o servidor:

```bash
uvicorn app.main:app --reload
```

### Endpoints principais

- `POST /api/v1/appointments`  
  Criar agendamento (Bot do WhatsApp). Header obrigatório `X-API-Key`.

- `GET /api/v1/appointments/my-agenda?employee_id=<uuid>`  
  Lista agenda ordenada por data/hora com paginação e `meta_ui` básico.

- `PATCH /api/v1/appointments/{id}/confirm?employee_id=<uuid>`  
  Confirma um agendamento.

- `PATCH /api/v1/appointments/{id}/cancel?employee_id=<uuid>&reason=...`  
  Cancela um agendamento com motivo opcional.


