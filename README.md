# Tarea_02_Progra3
# ✈️ Gestión de Vuelos con Lista Doblemente Enlazada + API REST

## 🎯 Objetivo del Proyecto

Desarrollar un sistema para gestionar vuelos en un aeropuerto utilizando:

- Una **Lista Doblemente Enlazada** para operaciones dinámicas.
- Una **base de datos SQLAlchemy** para persistencia.
- Una **API REST con FastAPI** para exposición de endpoints.

---

## 🧱 Tecnologías Usadas

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite (por simplicidad)
- Pydantic

---
## 📁 Estructura del Proyecto

```
gestor_vuelos/
├── app/
│   ├── __init__.py
│   ├── main.py               # Contiene los 8 endpoints requeridos
│   ├── models.py             # Modelo de datos Vuelo
│   ├── schemas.py            # Esquemas Pydantic
│   ├── crud.py               # Funciones ORM
│   ├── database.py           # Conexión a la base de datos
│   └── lista_doble.py        # Lista doblemente enlazada
├── vuelos.db                 # Base de datos local (SQLite)
├── requirements.txt
└── README.md
```

---

## 🧪 Cómo ejecutar el proyecto

1. Instala dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecuta el servidor:
```bash
uvicorn app.main:app --reload
```

3. Abre la documentación interactiva:
👉 http://127.0.0.1:8000/docs

---
