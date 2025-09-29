# note-keeper-167398-167416

FastAPI backend for a Notes application.

## Run locally

- Install dependencies:
  pip install -r notes_backend/requirements.txt

- Start server:
  uvicorn notes_backend.src.api.main:app --host 0.0.0.0 --port 3001 --reload

- API docs:
  - Swagger UI (themed): http://localhost:3001/docs-theme
  - ReDoc (themed): http://localhost:3001/redoc-theme
  - Default docs: http://localhost:3001/docs

## Environment variables

Provide these in a `.env` for production integration (do not commit secrets):

- ENVIRONMENT=development|production
- CORS_ALLOW_ORIGINS=http://localhost:3000,https://yourdomain.com
- NOTES_DB_URL= (optional; enables DB repository if set)
- NOTES_DB_USER= (optional)
- NOTES_DB_PASSWORD= (optional)
- NOTES_DB_NAME= (optional)
- NOTES_DB_PORT= (optional)

If NOTES_DB_URL is not set, an in-memory repository is used (data resets on restart).

## Notes

- Architecture highlights:
  - Routers in `src/api/routers`
  - Business logic in `src/api/services`
  - Persistence via repositories in `src/api/repositories` (DB placeholder included)
  - Pydantic models in `src/api/models`
  - Themed docs helpers in `src/api/core/docs.py`