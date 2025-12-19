# superhero-analytics
Análisis de superhéroes con Python

# 🦸 SuperHero Analytics Project (Python)

> **Análisis, filtrado y visualización de datos de superhéroes: desde JSON local hasta consumo de APIs e IA.**

Este proyecto simula un flujo de trabajo de desarrollo **end-to-end** profesional. Comienza con la ingestión de datos locales, aplica tipado estricto y lógica de negocio, visualiza resultados y evoluciona hacia el consumo de APIs externas (Marvel API) y generación de contenido con Inteligencia Artificial.

El proyecto está diseñado para ser reproducible, modular y fácilmente extensible.

---

## 📋 Tabla de Contenidos

1. [Estructura del Proyecto](#-estructura-del-proyecto)
2. [Prerrequisitos e Instalación](#-prerrequisitos-e-instalación)
3. [Ejecución](#-ejecución)
4. [Fases del Proyecto](#-fases-del-proyecto)
5. [Funcionalidades Principales](#-funcionalidades-principales)
6. [Visualizaciones](#-visualizaciones)
7. [Variables de Entorno][def]

---

## 📂 Estructura del Proyecto

```text
superhero-project/
│
├── data/
│   └── superheroes.json          # Dataset local (fase 1 a 3)
│
├── src/
│   ├── loader.py                 # Lectura y parseo de datos (ETL)
│   ├── models.py                 # Clases y tipado de personajes
│   ├── filters.py                # Lógica de ranking y balance
│   ├── search.py                 # Búsqueda de personajes
│   ├── plots.py                  # Gráficas y visualización
│   ├── image_ai.py               # Generación de imágenes IA (opcional)
│   └── app.py                    # Script maestro
│
├── requirements.txt              # Dependencias del proyecto
├── .env.sample                   # Variables de entorno (plantilla)
└── README.md                     # Este archivo
```

---

## ⚙️ Prerrequisitos e Instalación

Para garantizar la reproducibilidad, el proyecto está diseñado para ejecutarse en un entorno aislado con Conda.

**Requisitos:**
- Python 3.11 (mínimo)
- Conda (Gestor de entornos)

### 1. Configuración del Entorno

Ejecuta los siguientes comandos para crear el entorno `superhero` y activarlo:

```bash
# Crear ambiente con Python 3.11
conda create -n superhero python=3.11 -y

# Activar el ambiente
conda activate superhero
```

### 2. Instalación de Dependencias

Instala las librerías necesarias listadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecución

Para iniciar la aplicación principal, ejecuta el script maestro desde la raíz del proyecto:

```bash
python src/app.py
```

---

## 📅 Fases del Proyecto

### 🔹 Fase 1 — Lectura local desde JSON

- Ingesta de datos desde `data/superheroes.json`
- Visualización en consola de atributos obligatorios (Nombre, Cómics, etc.)
- Sin llamadas externas

### 🔹 Fase 2 — Trabajo con datos

- Transformación de datos a objetos Hero tipados
- Estructuración de atributos (powerstats, biography, appearance)
- Implementación de búsqueda por nombre

### 🔹 Fase 3 — Visualización

Generación de gráficas locales:
- Rankings por estadísticas
- Comparativas entre personajes
- Actualización dinámica según filtros

### 🔹 Fase 4 — Consumo de APIs (EXTERNA) 🌐

⚠️ **A partir de esta fase el proyecto requiere internet.**

- Sustitución del JSON local por la Marvel API
- Gestión de autenticación, paginación y control de errores

### 🔹 Fase Adicional (Opcional) 🤖

- Generación de imágenes mediante IA (DALL·E) basada en el nombre del superhéroe

---

## 🛠 Funcionalidades Principales

- **Filtrado Dinámico:** Selección por múltiples estadísticas
- **Rankings Inteligentes:**
  - 🏆 Top 10 más altos
  - 📉 Top 10 más bajos
  - ⚖️ Top 10 Balanceados: Desviación mínima respecto a la media
- **Búsqueda Incremental:** Por nombre
- **Visualización:** Imagen oficial o generada por IA

---

## 📊 Visualizaciones

El módulo de gráficas genera:

**Gráfica Principal (Barras Horizontales):**
- Eje Y: Nombre del superhéroe
- Eje X: Valor de la estadística
- Highlight: Resaltado visual del Top 1 y Top 3

**Vista Individual (Radar/Pastel):**
- Representación del balance general de estadísticas del personaje seleccionado

---

## 🔑 Variables de Entorno y APIs

Para las fases que consumen APIs externas (Fase 4 y Adicional), crea un archivo `.env` basado en la plantilla `.env.sample`:

```bash
cp .env.sample .env
```

Configura tus claves dentro del archivo `.env`:

```ini
SUPERHERO_TOKEN=tuTOKEN
OPENAI_API_KEY=tu_openai_key
```

---

## 📝 Notas Finales

- El proyecto escala de forma incremental; cada fase puede ejecutarse independientemente
- **Reproducibilidad:** Se prioriza Conda, pero es compatible con Docker o venv si se requiere
- La arquitectura separa lógica, vista y datos para facilitar el mantenimiento

[def]: #-variables-de-entorno-y-apis
