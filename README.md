# Event-Driven Notification Service

Backend orientado a eventos para gestionar notificaciones asíncronas con procesamiento en background.

Construido con una arquitectura sencilla pero realista usando **FastAPI + PostgreSQL + Redis + Celery + Docker**.

---

## Arquitectura

```text
Cliente
  |
  v
FastAPI API
  |
  | guarda notificación (queued)
  v
PostgreSQL
  |
  | encola tarea
  v
Redis (broker)
  |
  v
Celery Worker
  |
  | procesa envío
  v
PostgreSQL (status -> processing -> sent/failed)
```

---

## Features

- API REST con FastAPI
- Procesamiento asíncrono con Celery
- Redis como intermediario de mensajes para Celery
- PostgreSQL para persistencia
- Estados de ciclo de vida de notificaciones:
  - queued
  - processing
  - sent
  - failed
- Docker Compose para entorno local
- Health check de API + base de datos
- Tests con Pytest
- Arquitectura modular separando:
  - api
  - db
  - models
  - schemas
  - workers

---

## Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Celery
- Docker Compose
- Pytest

---

## Estructura del proyecto

```bash
.
├── app
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   ├── enums.py
│   │   └── notification.py
│   ├── schemas/
│   │   └── notification.py
│   ├── workers/
│   │   ├── celery_app.py
│   │   └── tasks.py
│   └── main.py
│
├── tests/
│   └── test_api.py
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "api": "up",
  "database": "up",
  "error": null
}
```

---

## Crear notificación

```http
POST /notifications
```

Payload:

```json
{
  "user_id": "42",
  "channel": "email",
  "payload": {
    "message": "hello"
  }
}
```

Response:

```json
{
  "id": "uuid",
  "status": "queued"
}
```

---

## Consultar notificación

```http
GET /notifications/{notification_id}
```

Ejemplo:

```json
{
  "id": "uuid",
  "user_id": "42",
  "channel": "email",
  "status": "sent",
  "payload": {
    "message": "hello"
  }
}
```

---

## Flujo asíncrono

Cuando se crea una notificación:

1. La API la persiste con estado `queued`
2. Se encola una tarea en Redis
3. Celery consume la tarea
4. El worker cambia estado a `processing`
5. Simula el envío
6. Marca la notificación como `sent`

Si falla:

```text
status -> failed
```

---

## Instalación

Clonar repo:

```bash
git clone https://github.com/Marcial-Godes/event-driven-notification-service.git
cd event-driven-notification-service
```

Crear entorno virtual:

```bash
python -m venv .venv
```

Activar:

Windows:

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Variables de entorno

Crear `.env` a partir del ejemplo:

Windows:

```bash
copy .env.example .env
```

Linux/Mac:

```bash
cp .env.example .env
```

---

## Levantar servicios

```bash
docker compose up -d
```

Servicios:

- PostgreSQL
- Redis

---

## Ejecutar API

```bash
uvicorn app.main:app --reload --reload-exclude .venv
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Ejecutar worker

Windows:

```bash
celery -A app.workers.tasks worker --pool=solo --loglevel=info
```

Nota:

En Windows se usa `--pool=solo` por compatibilidad.

---

## Tests

```bash
pytest -v
```

Actualmente:

- Health check
- Create notification
- Get notification

---

## Ejemplo de ejecución

Crear:

```json
{
 "status": "queued"
}
```

Worker:

```text
Sending notification ...
Notification ... sent
```

Consultar después:

```json
{
 "status": "sent"
}
```

---

## Diseño y decisiones

### ¿Por qué UUID?

Para sistemas distribuidos suele encajar mejor que ids secuenciales.

---

### ¿Por qué Redis + Celery?

Patrón clásico y probado para procesamiento en background.

Simple y robusto.

---

### ¿Por qué estados persistidos?

Permiten trazabilidad:

```text
queued -> processing -> sent
```

Y si algo falla:

```text
failed
```

---

## Mejoras futuras

Posibles extensiones:

- Retries automáticos con backoff
- Dead letter queue
- Rate limiting
- Email/SMS providers reales
- Autenticación
- Métricas y observabilidad
- Alembic migrations
- Dockerización completa de API y worker

---

## Ejemplo de ejecución local

Terminal 1:

```bash
docker compose up -d
```

Terminal 2:

```bash
uvicorn app.main:app --reload --reload-exclude .venv
```

Terminal 3:

```bash
celery -A app.workers.tasks worker --pool=solo --loglevel=info
```

---

## Estado del proyecto

Proyecto funcional:

- APIs backend
- procesamiento asíncrono
- arquitectura orientada a eventos
- integración con colas
- workers en background

---

## Autor

Marcial Godes

