# 📌 API REST con **FastAPI** y **SQLAlchemy**

## 📖 Descripción General
Este proyecto implementa una API RESTful con **FastAPI** utilizando **SQLAlchemy** como ORM y **SQL Server** como motor de base de datos.  

Se desarrolla sobre un caso hipotético de una escuela 📚 con **Estudiantes**, **Profesores** y **Materias**, permitiendo:  
- Registrar, buscar, actualizar y eliminar estudiantes, profesores y materias.  
- Consultar las notas de los estudiantes.  
- Calcular el promedio de notas por estudiante y materia.  

---

## 🏗️ Arquitectura del Proyecto

La estructura de carpetas es la siguiente:

📂 Proyecto

┣ 📂 database # Conexión a la base de datos (SQL Server)

┣ 📂 migrate # Scripts de migración para crear las tablas en la BD

┣ 📂 models # Modelos Pydantic y SQLAlchemy (tablas + respuestas)

┣ 📂 routers # Endpoints (CRUD y lógica de negocio)

┣ 📜 main.py # Punto de entrada de la aplicación

┣ 📜 requirements.txt

┣ 📜 test_connection.py # Validación de conexión a la BD


---

## ⚙️ Configuración Inicial

1. **Instalar dependencias**  
   Desde la raíz del proyecto, instala los requirements:  
   ```bash
   pip install -r requirements.txt

2. **Configurar la base de datos**  
    La base de datos debe llamarse: P1SW
    Actualiza las variables de conexión en database/connection.py según tu entorno

3. **Probar la conexión**  
    Ejecuta el script:
    ```bash
    python test_connection.py

    ✅ Si todo está correcto, verás un mensaje confirmando la conexión a SQL Server

4. **Migrar las tablas a la BD**  
    Desde la raíz del proyecto, corre:
    ```bash
    python -m migrate.database

5. **Levantar el servidor**  
    ```bash
    uvicorn main:app --reload

La API quedará disponible en: 👉 http://127.0.0.1:8000/docs

## 📚 Endpoints Principales

Estudiantes

POST /students/ → Crear estudiante

GET /students/ → Listar estudiantes

PUT /students/{id} → Actualizar estudiante

DELETE /students/{id} → Eliminar estudiante

Profesores

CRUD similar a estudiantes.

Materias

CRUD similar a estudiantes.

Notas

POST /notes/ → Registrar nota

GET /notes/average → Calcular promedio por estudiante y materia

## 🛠️ Tecnologías Usadas

FastAPI
 🚀 - Framework principal para la API.

SQLAlchemy
 🗄️ - ORM para manejar la BD.

SQL Server
 💾 - Motor de base de datos.

Uvicorn
 ⚡ - Servidor ASGI.

Pydantic
 🧩 - Validación de modelos.

Python-dotenv
 🔐 - Manejo de variables de entorno.