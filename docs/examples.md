# Tasks API — Ejemplos de request / response

Base URL local: `http://localhost:8000`
Prefijo de la API: `/api/task/`

Todos los cuerpos son JSON (`Content-Type: application/json`). Las fechas usan
ISO 8601 en UTC (ej. `2026-12-31T23:59:00Z`).

Estados permitidos (`status`): `pendiente`, `completada`, `pospuesta`.

**Autenticación:** todos los endpoints `/api/task/...` requieren un token JWT
en la cabecera `Authorization: Bearer <access>`. Sin token responden `401`.

---

## 0. Login — `POST /api/auth/token/`

Request:

```json
{ "email": "user@example.com", "password": "secret" }
```

Response `200 OK`:

```json
{ "access": "<jwt-access>", "refresh": "<jwt-refresh>" }
```

Renovación: `POST /api/auth/token/refresh/` con `{ "refresh": "<jwt-refresh>" }`.

---

## 1. Crear tarea — `POST /api/task/`

Request:

```json
{
  "title": "Escribir informe",
  "description": "Informe trimestral Q3",
  "status": "pendiente",
  "due_date": "2026-12-31T23:59:00Z",
  "created_by_name": "Andres"
}
```

Response `201 Created`:

```json
{
  "id": 1,
  "title": "Escribir informe",
  "description": "Informe trimestral Q3",
  "status": "pendiente",
  "due_date": "2026-12-31T23:59:00Z",
  "created_by": 1,
  "created_by_name": "Andres Rojas",
  "is_active": true,
  "created_at": "2026-07-03T23:24:10.032896Z",
  "updated_at": "2026-07-03T23:24:10.032915Z"
}
```

Campos: `title` es obligatorio; `description`, `status` (por defecto `pendiente`)
y `due_date` son opcionales. **El autor** (`created_by`) se toma siempre del
usuario del token, nunca del body; `created_by_name` se autocompleta con el
nombre/email del usuario si no se envía.

Errores de validacion:

```jsonc
// status invalido -> 400
{ "status": ["\"urgente\" is not a valid choice."] }

// due_date en el pasado -> 400
{ "errors": ["due_date cannot be in the past."] }
```

---

## 2. Listar tareas — `GET /api/task/list/`

Excluye por defecto las tareas eliminadas logicamente (`is_active = false`).

Filtros opcionales (query params):

| Param              | Ejemplo                          | Descripcion                          |
| ------------------ | -------------------------------- | ------------------------------------ |
| `status`           | `?status=pendiente`              | Filtra por estado exacto             |
| `search`           | `?search=informe`                | Busca en `title` y `description`     |
| `due_date_after`   | `?due_date_after=2026-01-01T00:00:00Z`  | Vencen a partir de esa fecha  |
| `due_date_before`  | `?due_date_before=2026-12-31T23:59:59Z` | Vencen antes de esa fecha     |
| `ordering`         | `?ordering=-due_date`            | Orden (`due_date`, `created_at`, `status`, `title`) |
| `page` / `limit`   | `?limit=10&page=0`               | Paginacion (LimitOffset)             |

Response `200 OK`:

```json
{
  "results": [
    {
      "id": 1,
      "title": "Escribir informe",
      "description": "Informe trimestral Q3",
      "status": "pendiente",
      "due_date": "2026-12-31T23:59:00Z",
      "created_by_name": "Andres",
      "is_active": true,
      "created_at": "2026-07-03T23:24:10.032896Z",
      "updated_at": "2026-07-03T23:24:10.032915Z"
    }
  ],
  "filtered": 1,
  "limit": 10,
  "total_pages": 1,
  "links": { "next": null, "previous": null },
  "count": 1
}
```

---

## 3. Actualizar tarea — `PUT /api/task/{id}/` o `PATCH /api/task/{id}/`

`PUT` reemplaza (requiere `title` y `status`); `PATCH` es parcial.

Request (`PATCH`):

```json
{ "title": "Escribir informe final" }
```

Response `200 OK`: la tarea completa actualizada (mismo formato que en la creacion).
Si el `id` no existe o esta eliminado -> `404 Not Found`.

---

## 4. Cambiar estado — `PATCH /api/task/{id}/status/`

Request:

```json
{ "status": "completada" }
```

Response `200 OK`: la tarea con el nuevo `status`.
Estado invalido -> `400`. Tarea inexistente -> `404`.

---

## 5. Eliminar tarea (logica) — `DELETE /api/task/{id}/`

Marca la tarea como inactiva (`is_active = false`) y rellena `deleted_at`; **no**
borra la fila. La tarea deja de aparecer en el listado.

Response `204 No Content` (sin cuerpo). Tarea inexistente -> `404`.

---

## 6. Tareas proximas a vencer — `GET /api/task/upcoming/`

Devuelve las tareas **activas y no completadas** cuyo `due_date` cae entre
**ahora** y **ahora + N dias**.

- `N` por defecto = `7` (configurable con `TASK_UPCOMING_DEFAULT_DAYS`).
- Se puede sobreescribir por peticion con `?days=`.

Ejemplos:

```
GET /api/task/upcoming/          # proximos 7 dias
GET /api/task/upcoming/?days=2   # proximas 48 horas
GET /api/task/upcoming/?days=1   # proximas 24 horas
```

Response `200 OK`: mismo formato paginado que el listado.

---

## 7. Auditoría / historial — `GET /api/task/{id}/history/`

Devuelve la traza completa registrada por `simple_history`: cada cambio con
**quién** (`history_user`), **cuándo** (`history_date`) y **tipo**
(`Created` / `Changed` / `Deleted`). Incluye tareas eliminadas lógicamente.
Ordenado del más reciente al más antiguo.

Response `200 OK`:

```json
[
  {
    "history_id": 3,
    "history_date": "2026-07-03T23:54:48.994Z",
    "history_type": "Changed",
    "history_user": "editor@example.com",
    "title": "Escribir informe",
    "status": "completada",
    "due_date": "2026-12-31T23:59:00Z",
    "is_active": true
  },
  {
    "history_id": 1,
    "history_date": "2026-07-03T23:54:48.824Z",
    "history_type": "Created",
    "history_user": "andres@example.com",
    "title": "Escribir informe",
    "status": "pendiente",
    "due_date": "2026-12-31T23:59:00Z",
    "is_active": true
  }
]
```

Tarea inexistente -> `404`.
