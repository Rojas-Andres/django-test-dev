# Tasks API — Prueba técnica (Python + Django + DRF + PostgreSQL)

API REST para gestionar una lista de tareas (to-do) con almacenamiento en
PostgreSQL, borrado lógico, control de estados, validaciones, documentación
Swagger/OpenAPI y colección Postman.

La lógica de negocio sigue la arquitectura DDD del stack (Cosmic Python):
capa pura en [`src/task/`](src/task) (domain / service_layer / adapters) y capa
Django/DRF en [`django_apps/task/`](django_apps/task).

## Requisitos

- **Python 3.10+** y **PostgreSQL 13+** (o Docker + Docker Compose).
- Dependencias en [`requirements/`](requirements) (`common.txt`, `development.txt`).

## Variables de entorno

Copia el ejemplo y ajústalo:

```bash
cp .env.example .env      # usado por docker compose (substitución de variables)
cp .env.example .envrc    # cargado dentro del contenedor worker (env_file)
```

Variables principales (ver [`.env.example`](.env.example)):

| Variable | Descripción |
| --- | --- |
| `DJANGO_SETTINGS_MODULE` | `django_project.settings.dev` |
| `DATABASE_HOST/PORT/NAME/USER/PASSWORD` | Conexión PostgreSQL |
| `POSTGRES_PORT_COMPOSE_EXPORT` | Puerto host donde se expone postgres |
| `TASK_UPCOMING_DEFAULT_DAYS` | Ventana por defecto de "próximas a vencer" (7) |

## Setup y ejecución

### Opción A — Docker (recomendada)

```bash
make build          # docker compose build
make up-d           # levanta postgres, redis y el worker (Django) en :8000
make migrate        # aplica migraciones
```

### Opción B — Entorno local (venv)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements/development.txt
# postgres local en marcha + variables exportadas (ver .env.example)
python manage.py migrate
python manage.py runserver 0:8000
```

## Comandos útiles

```bash
python manage.py migrate            # aplicar migraciones
python manage.py makemigrations     # generar migraciones
python manage.py test django_apps.task   # ejecutar los tests de la app tasks
```

## Documentación de la API (Swagger / OpenAPI)

Con el servidor en marcha:

- Swagger UI: http://localhost:8000/swagger
- Redoc: http://localhost:8000/redoc
- OpenAPI JSON/YAML: http://localhost:8000/swagger.json · http://localhost:8000/swagger.yaml

## Colección Postman

- Archivo: [`docs/postman_collection.json`](docs/postman_collection.json)
- Impórtala en Postman (*Import → File*). Incluye la variable `base_url`
  (`http://localhost:8000` por defecto) y `task_id`.
- Ejemplos de request/response por endpoint: [`docs/examples.md`](docs/examples.md).

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST | `/api/task/` | Crear tarea |
| GET | `/api/task/list/` | Listar (excluye eliminadas; filtros y orden) |
| PUT / PATCH | `/api/task/{id}/` | Actualizar (total / parcial) |
| PATCH | `/api/task/{id}/status/` | Cambiar sólo el estado |
| DELETE | `/api/task/{id}/` | Eliminación **lógica** |
| GET | `/api/task/upcoming/` | Tareas próximas a vencer |

**Modelo** `Task`: `id`, `title`, `description`, `status`
(`pendiente` / `completada` / `pospuesta`), `due_date`, `created_by_name`,
auditoría (`created_at`, `updated_at`) y borrado lógico (`is_active`,
`deleted_at`, heredados de `BaseModel`).

**Validaciones:** `title` obligatorio, `status` dentro de los permitidos y
`due_date` coherente (no puede estar en el pasado al crear). Los errores se
devuelven con el código HTTP adecuado (400 / 404) y un payload JSON.

## Criterio "próximas a vencer"

`GET /api/task/upcoming/` devuelve las tareas **activas y no completadas** cuyo
`due_date` está entre **ahora** y **ahora + N días**.

- `N` por defecto = **7 días** (`TASK_UPCOMING_DEFAULT_DAYS`).
- Se puede ajustar por petición con `?days=`:
  - `?days=1` → próximas 24 h · `?days=2` → 48 h · `?days=7` → 7 días.

---

# Stack for Django Projects by Andres Rojas

- Create alias
    - alias reset_docker='echo "Source .envrc" && source .envrc && echo "Down Docker" && make down && clear && echo "Down Build Docker" && make build && clear && echo "Up Detach" && make up-d'

- Documentacion arquitectura DDD
    - https://www.cosmicpython.com/book/part1.html

- Necesario para iniciar el proyecto
    - crear un role llamado RoleAWSAccess y darle permisos
    - Crear un bucket para guardar los templates
    - Crear la cola sqs en aws y guardarla en la siguiente envs
        -
- obtener access para acceder a los recursos de aws localmente

    - aws sts assume-role --role-arn arn:aws:iam::AWS_ACCOUNT_ID:role/RoleAWSAccess --role-session-name awscli --profile jumpcube --query "Credentials.[AccessKeyId,SecretAccessKey,SessionToken]" --output text | awk '{print "export AWS_ACCESS_KEY_ID="$1"\nexport AWS_SECRET_ACCESS_KEY="$2"\nexport AWS_SECURITY_TOKEN="$3""}' >> .envrc



# Build Fargate

- Error windows push ecr
    - https://stackoverflow.com/questions/60807697/docker-login-error-storing-credentials-the-stub-received-bad-data
        - Remove file docker-credential-wincred.exe C:\Program Files\Docker\Docker\resources\bin
        - Remove "credStore""credsStore"C:\Users\PROFILE_NAME\.docker\config.json
            - C:\Users\andre\.docker
    - O:\AA-DOWNLOAD-D\resources\bin


docker build --no-cache -t django:v1 .

- Probar local
    - docker run -p 8000:8000 django:v1

find . -type f -name "*.Identifier" -exec rm {} +