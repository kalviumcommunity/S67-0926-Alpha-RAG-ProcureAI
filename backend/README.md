# Procurement Document Intelligence API

Backend API for the procurement document intelligence system.

## Development

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start the development server:

```bash
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`

Swagger documentation: `http://127.0.0.1:8000/docs`

## Structure

- `app/api/` - API routes
- `app/core/` - application configuration
- `app/db/` - database infrastructure and models
- `app/schemas/` - API schemas
- `app/services/` - business/application services
- `app/storage/` - file storage functionality
- `uploads/` - development document uploads
