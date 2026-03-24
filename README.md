# FieldData Weather Alerts

API para gestionar alertas climáticas sobre campos agrícolas usando datos meteorológicos ya persistidos en base.

## Qué hace hoy

El proyecto ya tiene:

- modelo de datos base con migraciones
- datos demo para `users`, `fields` y `weather_forecasts`
- endpoints para consultar forecasts, alertas y notificaciones
- creación y actualización de alertas
- evaluación manual de alertas para generar notificaciones

## Flujo rápido

El flujo principal de uso es este:

1. Consultar los forecasts disponibles.
2. Crear una alerta para un `field_id` existente.
3. Ejecutar la evaluación de alertas.
4. Consultar las notificaciones generadas.

## Endpoints principales

### `GET /`

Healthcheck simple de la aplicación.

### `GET /api/v1/health`

Healthcheck dentro del prefijo de API.

### `GET /api/v1/weather-forecasts/`

Lista los datos meteorológicos mockeados que ya existen en base.

Se usa para entender:

- qué `field_id` existen
- qué `event_type` existen
- qué probabilidades podrían disparar alertas

### `GET /api/v1/alerts/`

Lista todas las alertas creadas.

### `POST /api/v1/alerts/`

Crea una nueva alerta.

Body esperado:

```json
{
  "field_id": 1,
  "event_type": "rain",
  "threshold": 70
}
```

Reglas principales:

- `field_id` debe existir
- `event_type` debe ser uno de los valores válidos
- `threshold` debe estar entre `0` y `100`

### `PATCH /api/v1/alerts/{alert_id}`

Actualiza una alerta existente.

Permite modificar:

- `threshold`
- `is_active`

Ejemplo:

```json
{
  "threshold": 60,
  "is_active": true
}
```

### `POST /api/v1/alerts/evaluate`

Ejecuta manualmente la evaluación de alertas activas contra los forecasts futuros.

Si una alerta supera el umbral:

- se genera una notificación
- no se duplica si ya existe una para la misma combinación `alert + forecast`

Respuesta esperada:

```json
{
  "processed_alerts": 2,
  "notifications_created": 1
}
```

### `GET /api/v1/notifications/`

Lista las notificaciones generadas por la evaluación.

## Orden recomendado para probarlo

1. `GET /api/v1/weather-forecasts/`
2. `POST /api/v1/alerts/`
3. `GET /api/v1/alerts/`
4. `POST /api/v1/alerts/evaluate`
5. `GET /api/v1/notifications/`

## Ejemplo que debería disparar una notificación

Con los datos demo actuales, esta alerta debería matchear:

```json
{
  "field_id": 1,
  "event_type": "rain",
  "threshold": 70
}
```

Porque en los datos seed existe un forecast para `field_id=1`, evento `rain`, con probabilidad `72`.

## Validaciones y errores esperables

La API ahora devuelve errores con un formato uniforme:

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

- `400` para errores de negocio, por ejemplo si el `field_id` no existe
- `404` si se intenta actualizar una alerta inexistente
- `422` si el body tiene tipos inválidos o faltan campos requeridos
- `500` con un mensaje genérico si ocurre un problema interno no controlado

Ejemplos:

- `field_id` inexistente al crear alerta: `400`
- `threshold` fuera de rango: `422`
- mandar texto donde se espera número: `422`

Un `500` no debería representar un error de input del usuario; si aparece, la respuesta no expone detalles internos, pero indica que hubo un fallo del servidor.
# FieldData-challenge
