# API de Gestión de Rutas y Transporte Escolar

API REST desarrollada con **FastAPI** para administrar la operación de un servicio de transporte escolar. El proyecto permite registrar usuarios, acudientes, estudiantes, conductores, vehículos, rutas, paraderos, asignaciones de estudiantes a rutas y eventos de abordaje.

La aplicación utiliza **SQLAlchemy** para comunicarse con una base de datos PostgreSQL, configurada actualmente mediante una conexión a Supabase.

## Resumen rápido

El flujo general del sistema es:

```text
Cliente (Swagger, navegador o frontend)
        |
        v
      FastAPI / Uvicorn
        |
        v
   Routers + Pydantic
        |
        v
     SQLAlchemy
        |
        v
      PostgreSQL / Supabase
```

La API no guarda los datos en archivos locales. Cuando una operación de escritura termina correctamente, SQLAlchemy ejecuta `commit()` y el registro queda almacenado en las tablas PostgreSQL del proyecto Supabase configurado en `DATABASE_URL`.

## 1. ¿Para qué sirve?

El sistema centraliza la información necesaria para organizar y controlar el transporte escolar:

- Define los roles y usuarios que operan el sistema.
- Registra los acudientes responsables de los estudiantes.
- Registra estudiantes y los vincula con sus acudientes.
- Administra conductores, sus licencias y su estado activo.
- Administra vehículos y su capacidad o disponibilidad.
- Crea rutas con horarios, conductor y vehículo asignados.
- Registra los paraderos de cada servicio.
- Asigna cada estudiante a una ruta y a un paradero.
- Guarda registros de abordaje asociados a estudiantes y rutas.
- Expone documentación interactiva para probar la API.

## 2. Tecnologías utilizadas

- **Python**: lenguaje de programación.
- **FastAPI**: framework para construir la API REST y generar documentación OpenAPI.
- **Uvicorn**: servidor ASGI recomendado para ejecutar FastAPI.
- **SQLAlchemy**: ORM utilizado para representar las tablas y ejecutar consultas.
- **Pydantic**: validación de los datos de entrada y salida mediante esquemas.
- **python-dotenv**: carga las variables definidas en el archivo `.env`.
- **PostgreSQL/Supabase**: base de datos relacional utilizada por la aplicación.

## 3. Estructura del proyecto

```text
gestion-transporte-api/
├── .env
├── database.py
├── main.py
├── models.py
├── schemas.py
├── routers/
│   ├── acudientes.py
│   ├── conductores.py
│   ├── estudiante_ruta.py
│   ├── estudiantes.py
│   ├── paraderos.py
│   ├── registros_abordaje.py
│   ├── roles.py
│   ├── rutas.py
│   ├── usuarios.py
│   └── vehiculos.py
└── venv/
```

### `.env`

Contiene la configuración sensible de la conexión a la base de datos. Para este backend Python, la variable que realmente se utiliza es `DATABASE_URL`:

```env
DATABASE_URL=postgresql://usuario:contraseña@servidor:puerto/base_de_datos
```

El archivo no debe subirse a Git ni compartirse públicamente. En un entorno real conviene crear un `.env.example` sin la contraseña para indicar qué variables necesita el proyecto.

`database.py` busca esta variable con `os.getenv("DATABASE_URL")`. Por eso la URL debe escribirse en `.env` y nunca como código Python. La forma incorrecta sería:

```python
DATABASE_URL = os.getenv("postgresql://...")
```

La forma correcta es:

```python
DATABASE_URL = os.getenv("DATABASE_URL")
```

La conexión PostgreSQL debe copiarse desde **Supabase → Connect**, preferiblemente usando el pooler que indique Supabase para conexiones externas. La URL del proyecto (`SUPABASE_URL`) y la clave publicable no sustituyen a `DATABASE_URL`; son valores para clientes Supabase y actualmente no son leídos por este backend.

### `database.py`

Configura la conexión con PostgreSQL:

1. Carga las variables del archivo `.env` con `load_dotenv()`.
2. Lee `DATABASE_URL` del entorno.
3. Crea `engine`, que administra la conexión con la base de datos.
4. Crea `SessionLocal`, una fábrica de sesiones SQLAlchemy.
5. Crea `Base`, clase base para todos los modelos.
6. Define `get_db()`, una dependencia de FastAPI que abre una sesión para cada solicitud y la cierra al terminar.

La función `get_db()` se utiliza en los routers mediante `Depends(get_db)`. Esto evita mantener una conexión abierta innecesariamente.

Importante: este archivo configura el acceso a la base de datos, pero no crea las tablas. Las tablas deben existir previamente en Supabase/PostgreSQL. Si `DATABASE_URL` falta, la aplicación detiene el inicio con un error claro.

### `models.py`

Contiene los modelos ORM de SQLAlchemy. Cada clase representa una tabla de la base de datos y cada atributo `Column` representa una columna.

Modelos disponibles:

| Modelo | Tabla | Propósito |
|---|---|---|
| `Rol` | `roles` | Tipos de permisos o perfiles de usuario. |
| `Usuario` | `usuarios` | Personas que utilizan o administran el sistema. |
| `Acudiente` | `acudientes` | Responsables de los estudiantes y usuario que los registra. |
| `Estudiante` | `estudiantes` | Niños o jóvenes que usan el transporte. |
| `Conductor` | `conductores` | Conductores asignables a las rutas. |
| `Vehiculo` | `vehiculos` | Buses o vehículos del servicio. |
| `Ruta` | `rutas` | Servicios de transporte con horario, conductor y vehículo. |
| `Paradero` | `paraderos` | Lugares donde se recoge o deja a los estudiantes. |
| `EstudianteRuta` | `estudiante_ruta` | Asignación de estudiante, ruta y paradero. |
| `RegistroAbordaje` | `registros_abordaje` | Historial de eventos de abordaje. |

Relaciones principales:

- Un `Rol` puede tener muchos `Usuario`.
- Un `Usuario` puede estar asociado con muchos `Acudiente`.
- Un `Acudiente` puede estar relacionado con muchos `Estudiante`.
- Cada `Estudiante` pertenece a un `Acudiente`.
- Cada `Ruta` referencia un `Conductor` y un `Vehiculo`.
- `EstudianteRuta` conecta un estudiante con una ruta y un paradero.
- `RegistroAbordaje` identifica al estudiante y la ruta del evento.

### Conexión entre todas las tablas

Todas las tablas están conectadas mediante claves foráneas. La relación completa puede verse así:

```text
roles 1 ─────── N usuarios 1 ─────── N acudientes
acudientes 1 ── N estudiantes
conductores 1 ─ N rutas N ───── 1 vehiculos
       │
estudiantes 1 ───────────┼── N estudiante_ruta N ── 1 paraderos
  │                │
  └── N registros_abordaje N ───────────────┘
```

La tabla `estudiante_ruta` es la tabla intermedia que conecta estudiantes, rutas y paraderos. Por eso, aunque `paraderos` no tiene una clave foránea directa hacia `rutas`, sí queda conectada a ellas a través de la asignación. La cadena completa comienza en `roles`, continúa por `usuarios` y `acudientes`, y desde los acudientes llega a estudiantes, rutas, conductores, vehículos, paraderos y registros de abordaje.

El SQL también impide repetir exactamente la misma asignación de estudiante, ruta y paradero mediante la restricción `UNIQUE (estudiante_id, ruta_id, paradero_id)`.

Las claves foráneas garantizan que estas referencias apunten a registros relacionados. Los campos `id` son claves primarias y tienen índices configurados.

## 4. Tablas y campos

Los nombres de las columnas deben coincidir con los siguientes. Los campos marcados como obligatorios no pueden omitirse al crear o actualizar mediante la API.

| Tabla | Campos principales |
|---|---|
| `roles` | `id`, `nombre` obligatorio y único, `descripcion` opcional. |
| `usuarios` | `id`, `nombre`, `apellido`, `correo` obligatorio y único, `telefono`, `rol_id`. |
| `acudientes` | `id`, `nombre`, `apellido`, `documento` obligatorio y único, `telefono`, `correo`, `usuario_id`. |
| `estudiantes` | `id`, `nombre`, `apellido`, `documento` obligatorio y único, `grado`, `direccion`, `acudiente_id`. |
| `conductores` | `id`, `nombre`, `apellido`, `documento` único, `licencia` única, `telefono`, `activo`. |
| `vehiculos` | `id`, `placa` única, `marca`, `modelo`, `capacidad`, `estado`. |
| `rutas` | `id`, `nombre` único, `descripcion`, `hora_salida`, `hora_llegada`, `conductor_id`, `vehiculo_id`, `estado`. |
| `paraderos` | `id`, `nombre`, `direccion`, `referencia`, `latitud`, `longitud`. |
| `estudiante_ruta` | `id`, `estudiante_id`, `ruta_id`, `paradero_id`; la combinación de los tres IDs es única. |
| `registros_abordaje` | `id`, `estudiante_id`, `ruta_id`, `fecha_hora`, `tipo`. |

Detalles de formato:

- `documento` es `str`, por lo que puede escribirse como `TI100200021`, `CC100200021` u otro formato definido por el proyecto.
- `grado` también es `str`; son válidos valores como `7`, `7A` o `7°`.
- `hora_salida` y `hora_llegada` usan formato de hora, por ejemplo `06:30:00`.
- `latitud` y `longitud` aceptan números decimales.
- `activo` acepta `true` o `false`.
- `fecha_hora` se genera automáticamente en la base de datos al crear un abordaje si no se envía desde la API.

### `schemas.py`

Define los esquemas Pydantic usados para validar y serializar la información de la API.

Para cada recurso normalmente existen tres clases:

- `...Base`: campos comunes del recurso.
- `...Create`: estructura esperada al crear o actualizar. Actualmente hereda de `Base` sin añadir campos.
- `...Response`: datos devueltos al cliente, incluyendo el `id`.

Las clases `Response` usan `from_attributes = True`, lo que permite convertir objetos SQLAlchemy en respuestas JSON de FastAPI.

Tipos importantes:

- `Optional[str]`: campo de texto opcional.
- `int`: identificadores, capacidad y claves foráneas.
- `bool`: estado activo de un conductor.
- `time`: horas de salida y llegada de una ruta.
- `float`: coordenadas de un paradero.
- `datetime`: fecha y hora de un abordaje.

Pydantic rechaza solicitudes que no cumplen los tipos requeridos antes de que lleguen a la lógica del endpoint.

### `main.py`

Es el punto de entrada de la aplicación.

1. Crea la instancia `FastAPI` con título, descripción y versión.
2. Importa los routers de cada módulo funcional.
3. Registra los routers mediante `app.include_router(...)`.
4. Define `GET /`, que confirma que la API está activa.
5. Define `GET /prueba-db`, que ejecuta `SELECT 1` para comprobar la conexión con Supabase.

### `routers/`

Cada archivo dentro de esta carpeta agrupa los endpoints de una entidad. El patrón general es:

1. Recibir y validar el cuerpo con un esquema Pydantic.
2. Obtener una sesión con `Depends(get_db)`.
3. Consultar o modificar el modelo SQLAlchemy.
4. Confirmar los cambios con `commit()`.
5. Actualizar el objeto con `refresh()`.
6. Devolver el resultado usando el esquema de respuesta.

Los endpoints que buscan un registro por ID devuelven `404` cuando no lo encuentran.

## 5. Endpoints disponibles

Todos los endpoints terminan en `/`. Por ejemplo, la colección de estudiantes es `GET /estudiantes/`.

### Sistema y base de datos

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Comprueba que la API está funcionando. |
| `GET` | `/prueba-db` | Ejecuta una consulta simple contra la base de datos. |

### Roles

Archivo: `routers/roles.py`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/roles/` | Lista todos los roles. |
| `POST` | `/roles/` | Crea un rol. |

Los roles no tienen actualmente endpoints para consultar uno, actualizarlo o eliminarlo.

### Usuarios

Archivo: `routers/usuarios.py`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/usuarios/` | Lista usuarios. |
| `GET` | `/usuarios/{usuario_id}` | Obtiene un usuario por ID. |
| `POST` | `/usuarios/` | Crea un usuario. |
| `PUT` | `/usuarios/{usuario_id}` | Reemplaza los datos de un usuario. |
| `DELETE` | `/usuarios/{usuario_id}` | Elimina un usuario. |

### Acudientes

Archivo: `routers/acudientes.py`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/acudientes/` | Lista acudientes. |
| `GET` | `/acudientes/{acudiente_id}` | Obtiene un acudiente por ID. |
| `POST` | `/acudientes/` | Crea un acudiente. |
| `PUT` | `/acudientes/{acudiente_id}` | Actualiza un acudiente. |
| `DELETE` | `/acudientes/{acudiente_id}` | Elimina un acudiente. |

### Estudiantes

Archivo: `routers/estudiantes.py`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/estudiantes/` | Lista estudiantes. |
| `GET` | `/estudiantes/{estudiante_id}` | Obtiene un estudiante por ID. |
| `POST` | `/estudiantes/` | Crea un estudiante y evita documentos duplicados. |
| `PUT` | `/estudiantes/{estudiante_id}` | Actualiza un estudiante. |
| `DELETE` | `/estudiantes/{estudiante_id}` | Elimina un estudiante. |

### Conductores

Archivo: `routers/conductores.py`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/conductores/` | Lista conductores. |
| `GET` | `/conductores/{conductor_id}` | Obtiene un conductor por ID. |
| `POST` | `/conductores/` | Crea un conductor. |
| `PUT` | `/conductores/{conductor_id}` | Actualiza un conductor. |
| `DELETE` | `/conductores/{conductor_id}` | Elimina un conductor. |

### Vehículos

Archivo: `routers/vehiculos.py`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/vehiculos/` | Lista vehículos. |
| `GET` | `/vehiculos/{vehiculo_id}` | Obtiene un vehículo por ID. |
| `POST` | `/vehiculos/` | Crea un vehículo. |
| `PUT` | `/vehiculos/{vehiculo_id}` | Actualiza un vehículo. |
| `DELETE` | `/vehiculos/{vehiculo_id}` | Elimina un vehículo. |

### Rutas

Archivo: `routers/rutas.py`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/rutas/` | Lista rutas. |
| `GET` | `/rutas/{ruta_id}` | Obtiene una ruta por ID. |
| `POST` | `/rutas/` | Crea una ruta. |
| `PUT` | `/rutas/{ruta_id}` | Actualiza una ruta. |
| `DELETE` | `/rutas/{ruta_id}` | Elimina una ruta. |

### Paraderos

Archivo: `routers/paraderos.py`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/paraderos/` | Lista paraderos. |
| `GET` | `/paraderos/{paradero_id}` | Obtiene un paradero por ID. |
| `POST` | `/paraderos/` | Crea un paradero. |
| `PUT` | `/paraderos/{paradero_id}` | Actualiza un paradero. |
| `DELETE` | `/paraderos/{paradero_id}` | Elimina un paradero. |

### Asignaciones estudiante-ruta

Archivo: `routers/estudiante_ruta.py`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/estudiante-ruta/` | Lista asignaciones. |
| `GET` | `/estudiante-ruta/{asignacion_id}` | Obtiene una asignación por ID. |
| `POST` | `/estudiante-ruta/` | Asigna un estudiante a una ruta y paradero. |
| `PUT` | `/estudiante-ruta/{asignacion_id}` | Actualiza una asignación. |
| `DELETE` | `/estudiante-ruta/{asignacion_id}` | Elimina una asignación. |

### Registros de abordaje

Archivo: `routers/registros_abordaje.py`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/registros-abordaje/` | Lista registros de abordaje. |
| `GET` | `/registros-abordaje/{registro_id}` | Obtiene un registro por ID. |
| `POST` | `/registros-abordaje/` | Crea un registro con tipo de evento. |
| `PUT` | `/registros-abordaje/{registro_id}` | Actualiza un registro. |
| `DELETE` | `/registros-abordaje/{registro_id}` | Elimina un registro. |

## 6. Instalación y ejecución

### Requisitos

- Python 3.9 o superior.
- Una base de datos PostgreSQL accesible.
- Las tablas correspondientes a los modelos creadas en la base de datos.

### Crear y activar el entorno virtual en Windows

Desde la carpeta raíz del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, se puede ejecutar la API directamente con `venv\Scripts\python.exe` o ajustar la política de ejecución de PowerShell según la configuración del equipo.

### Instalar dependencias

Como el repositorio todavía no incluye `requirements.txt`, instala las dependencias importadas por el código:

```powershell
pip install fastapi uvicorn sqlalchemy python-dotenv psycopg2-binary
```

`psycopg2-binary` es el controlador habitual para una URL de PostgreSQL. Si la URL o el proveedor requiere otro controlador, debe ajustarse la dependencia y el formato de conexión.

### Configurar el `.env`

Crea o completa `.env` en la raíz:

```env
DATABASE_URL=postgresql://usuario:contraseña@host:5432/postgres
```

La contraseña debe estar correctamente codificada en URL si contiene espacios o caracteres especiales. No publiques este valor.

### Iniciar el servidor

```powershell
uvicorn main:app --reload
```

La API quedará disponible normalmente en:

```text
http://127.0.0.1:8000
```

También puede iniciarse usando el Python del entorno virtual:

```powershell
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

Si el puerto `8000` está ocupado por otra instancia de Uvicorn, inicia la API en otro puerto:

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

En ese caso, la dirección de Swagger será `http://127.0.0.1:8001/docs`.

## 7. Documentación interactiva

FastAPI genera automáticamente:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Especificación OpenAPI: `http://127.0.0.1:8000/openapi.json`

Desde Swagger UI se pueden consultar los endpoints, ver los esquemas esperados y enviar solicitudes de prueba.

## 8. Cómo usar Swagger paso a paso

1. Inicia la API con Uvicorn.
2. Abre `/docs` en el puerto que aparezca en la terminal.
3. Selecciona un recurso, por ejemplo **Estudiantes**.
4. Abre `GET /estudiantes/` y presiona **Try it out**.
5. Presiona **Execute** para traer todos los estudiantes.
6. Para traer uno, usa `GET /estudiantes/{estudiante_id}`, escribe un ID y presiona **Execute**.
7. Para insertar, actualizar o eliminar, abre el método correspondiente y usa **Try it out**.

Un código `200` indica que la consulta terminó correctamente. Swagger es solamente la interfaz de prueba: los datos los consulta o modifica el backend en Supabase.

## 9. Ejemplos de solicitudes

### Crear un acudiente

```http
POST /acudientes/
Content-Type: application/json

{
  "nombre": "Laura",
  "apellido": "Gomez",
  "documento": "1000000001",
  "telefono": "3000000000",
  "correo": "laura@example.com",
  "usuario_id": 1
}
```

### Crear un estudiante

El `acudiente_id` debe corresponder a un acudiente existente. El tipo de documento y el grado se envían como texto.

```http
POST /estudiantes/
Content-Type: application/json

{
  "nombre": "Carlos",
  "apellido": "Gomez",
  "documento": "TI100200021",
  "grado": "7A",
  "direccion": "Carrera 10 # 20-30",
  "acudiente_id": 1
}
```

Respuesta esperada:

```json
{
  "id": 21,
  "nombre": "Carlos",
  "apellido": "Gomez",
  "documento": "TI100200021",
  "grado": "7A",
  "direccion": "Carrera 10 # 20-30",
  "acudiente_id": 1
}
```

### Crear una ruta

El conductor y el vehículo deben existir antes de crear la ruta.

```http
POST /rutas/
Content-Type: application/json

{
  "nombre": "Ruta Norte",
  "descripcion": "Recorrido por el sector norte",
  "hora_salida": "06:30:00",
  "hora_llegada": "07:20:00",
  "conductor_id": 1,
  "vehiculo_id": 1,
  "estado": "Activa"
}
```

### Registrar un abordaje

```http
POST /registros-abordaje/
Content-Type: application/json

{
  "estudiante_id": 1,
  "ruta_id": 1,
  "tipo": "Subida"
}
```

La fecha y hora se generan en la base de datos mediante `CURRENT_TIMESTAMP` cuando se crea el registro.

## 10. Flujo recomendado de uso

1. Crear los roles.
2. Crear los usuarios y asignarles un `rol_id`.
3. Crear los acudientes.
4. Crear los estudiantes asociados a sus acudientes.
5. Registrar conductores y vehículos.
6. Crear los paraderos.
7. Crear las rutas con conductor y vehículo.
8. Crear las asignaciones en `estudiante-ruta`.
9. Registrar cada evento de abordaje.

Este orden reduce errores de claves foráneas porque las entidades referenciadas existen antes de crear sus relaciones.

## 11. Qué significa cada respuesta

| Código | Significado |
|---|---|
| `200` | Operación exitosa. En `GET` devuelve datos; en `POST`/`PUT` devuelve el registro guardado. |
| `404` | El ID solicitado no existe. |
| `400` | Error de regla implementada, como un documento de estudiante duplicado. |
| `422` | El JSON no cumple el esquema Pydantic: falta un campo o tiene un tipo incorrecto. |
| `409` o error de integridad | Conflicto con una restricción única o una clave foránea de PostgreSQL. |
| `500` | Error del servidor, normalmente relacionado con conexión, configuración o estructura de la base. |

## 12. Validaciones y respuestas

- Los campos definidos como obligatorios deben enviarse en el JSON.
- Los campos opcionales pueden omitirse o enviarse como `null`.
- Los IDs de las rutas se reciben como enteros en la URL.
- Las horas de ruta deben respetar el formato de hora aceptado por Pydantic, por ejemplo `06:30:00`.
- Los registros inexistentes producen una respuesta HTTP `404`.
- Los datos con tipos incorrectos normalmente producen una respuesta HTTP `422` generada por FastAPI.
- Las restricciones `unique` de la base de datos impiden repetir correos, documentos, licencias, placas o nombres únicos.
- Las operaciones de escritura ejecutan `commit()` y luego `refresh()` para devolver el registro persistido.

## 13. Estado actual y aspectos pendientes

El proyecto ya contiene la API funcional básica, pero actualmente no incluye:

- Archivo `requirements.txt` o equivalente para instalar dependencias automáticamente.
- Migraciones de base de datos con Alembic.
- Creación automática de tablas.
- Autenticación, autorización por rol o tokens JWT.
- Paginación, filtros o búsquedas avanzadas.
- Manejo centralizado de errores de integridad de base de datos.
- Validaciones de negocio como verificar capacidad del vehículo o impedir asignaciones duplicadas.
- Relaciones ORM explícitas en todos los modelos relacionados.
- Pruebas automatizadas.

Estas funciones pueden agregarse como siguientes etapas sin cambiar la idea principal de la estructura actual.

## 14. Buenas prácticas para continuar el proyecto

- Mantener las credenciales únicamente en variables de entorno.
- Crear un `requirements.txt` con las versiones probadas.
- Añadir `.env` y `venv/` al `.gitignore`.
- Usar Alembic para controlar cambios en el esquema de la base de datos.
- Agregar pruebas para cada endpoint y para los casos `404`, duplicados y claves foráneas inválidas.
- Implementar autenticación antes de exponer la API en producción.
- Usar un dominio o prefijo de versión, por ejemplo `/api/v1`, cuando la API crezca.