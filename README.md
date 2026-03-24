# FieldData Weather Alerts

Backend para el challenge de alertas climaticas usando FastAPI, SQLAlchemy async, PostgreSQL y Alembic.

La aplicacion trabaja sobre forecasts climaticos futuros ya almacenados en base de datos. Un usuario crea una alerta asociada a un campo, un tipo de evento climatico y un `threshold`. El `threshold` representa el valor minimo de probabilidad a partir del cual el usuario quiere ser avisado. Por ejemplo, si una alerta para lluvia tiene `threshold=70`, la notificacion solo se genera cuando exista un weather forecast de lluvia para ese campo con probabilidad mayor o igual a `70`.

La evaluacion de alertas puede ejecutarse manualmente por endpoint o automaticamente mediante un background job. Cuando la probabilidad del forecast supera el `threshold` configurado, el sistema crea una notificacion. La aplicacion evita duplicados para la misma combinacion de alerta y forecast. No hay integracion real con WhatsApp: la tabla `notifications` representa la salida lista para un envio futuro, incluyendo `channel`, `recipient`, `status` y `message`.

## Como levantar el proyecto

1. Duplicar `.env.template`.
2. Dejar una de esas copias con el nombre `.env`.
3. Completar o ajustar las variables de entorno en ese archivo `.env`.

Variables principales:

- `PROJECT_NAME`
- `API_PREFIX`
- `APP_HOST`
- `APP_PORT`
- `LOG_LEVEL`
- `POSTGRES_SERVER`
- `POSTGRES_PORT`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `DATABASE_URL`
- `ALERT_EVALUATION_INTERVAL_SECONDS`

Levantar PostgreSQL:

```bash
docker compose up -d db
```

Preparar entorno local:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

Correr migraciones:

Local:

```bash
alembic upgrade head
```

Con Docker:

```bash
docker compose run --rm api alembic upgrade head
```

Levantar la API:

Local:

```bash
fastapi dev
```

Con Docker:

```bash
docker compose up -d api
```
En la consola se pueden obreservar logs informativos para ver cuando es que corre el job, cuando se ejecutan ciertos metodos, etc.

Swagger UI para ver la documentacion de los endpoints y probarlos desde ahi:

```text
http://127.0.0.1:8000/docs
```

## Charts

En mermaid_chart.md se encuentran los diagramas de la app y de la db.

## Endpoints principales

Todos los endpoints quedan bajo el prefijo `/agrobot`.

### `GET /agrobot/weather-forecasts`

Lista los forecasts disponibles en base.

Respuesta:

- lista de forecasts
- cada forecast incluye `field_id`, `event_type`, `forecast_date`, `probability`, `source`

### `GET /agrobot/alerts`

Lista las alertas creadas.

Respuesta:

- lista de alertas
- cada alerta incluye `field_id`, `event_type`, `threshold`, `is_active`

### `POST /agrobot/alerts`

Crea una nueva alerta.

Body:

```json
{
  "field_id": 1,
  "event_type": "rain",
  "threshold": 70
}
```

Reglas:

- `field_id` debe existir
- `event_type` debe ser uno de los valores validos
- `threshold` debe estar entre `0` y `100`

### `PATCH /agrobot/alerts/{alert_id}`

Actualiza una alerta existente.

Params:

- `alert_id`: id de la alerta

Body:

```json
{
  "threshold": 60,
  "is_active": true
}
```

Se puede enviar uno o ambos campos:

- `threshold`
- `is_active`

### `POST /agrobot/alerts/evaluate`

Ejecuta manualmente la evaluacion de alertas activas contra los forecasts futuros.

Body:

- no requiere body

Respuesta:

```json
{
  "processed_alerts": 2,
  "notifications_created": 1
}
```

### `GET /agrobot/notifications`

Lista las notificaciones generadas.

Respuesta:

- lista de notificaciones
- cada una incluye `channel`, `recipient`, `status`, `message`

## Flujo recomendado para probarlo

1. Consultar `GET /agrobot/weather-forecasts` para ver que datos existen.
2. Crear una alerta con `POST /agrobot/alerts`.
3. Verificarla con `GET /agrobot/alerts`.
4. Ejecutar `POST /agrobot/alerts/evaluate`. O esperar 60 segundos a que corra el job
5. Consultar `GET /agrobot/notifications`.

Con los datos demo actuales, una alerta para `field_id=1`, `event_type=rain`, `threshold=70` deberia generar una notificacion.

## Errores esperables

La API devuelve errores con formato uniforme:

```json
{
  "error": {
    "code": "validation_error",
    "message": "The request contains invalid or missing data.",
    "details": [
      {
        "field": "threshold",
        "message": "Input should be less than or equal to 100"
      }
    ]
  }
}
```

Comportamiento actual:

- `400` para errores de negocio, por ejemplo `field_id` inexistente
- `404` para recursos inexistentes
- `422` para body invalido o tipos incorrectos
- `500` para errores internos no controlados

## Tests

La suite usa SQLite async en memoria para no depender de PostgreSQL.

```bash
python -m pytest
```

## Logging

El proyecto usa `logging` de Python con logs en:

- arranque y parada del scheduler
- iteraciones del background job
- creacion y actualizacion de alertas
- evaluacion de alertas y creacion de notificaciones
- warnings para validaciones de negocio rechazadas
