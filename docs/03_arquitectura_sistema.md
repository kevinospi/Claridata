# Arquitectura del Sistema

## Objetivo

StatMindAI se diseña como una plataforma de análisis estadístico asistida por inteligencia artificial, donde los cálculos estadísticos son realizados por herramientas especializadas y la IA se encarga de interpretar resultados, explicar conceptos y comprender la intención del usuario.

## Componentes Principales

### Frontend

Responsabilidades:

* Interfaz de usuario.
* Carga de archivos.
* Visualización de resultados.
* Visualización de gráficos.

### Backend (FastAPI)

Responsabilidades:

* Exponer la API REST.
* Validar peticiones.
* Coordinar los componentes internos.
* Gestionar el flujo de procesamiento.

### Motor Estadístico

Responsabilidades:

* Leer datasets.
* Calcular estadísticas descriptivas.
* Generar visualizaciones.
* Ejecutar análisis estadísticos.

Tecnologías previstas:

* Pandas
* NumPy
* SciPy
* Statsmodels
* Matplotlib

### Motor IA

Responsabilidades:

* Explicar conceptos.
* Interpretar resultados.
* Comprender consultas en lenguaje natural.
* Resolver sinónimos y equivalencias.

## Flujo de Aprendizaje

Usuario
→ Frontend
→ Backend
→ Motor IA
→ Usuario

## Flujo de Análisis

Usuario
→ Frontend
→ Backend
→ Motor Estadístico
→ Motor IA
→ Usuario

## Principio Arquitectónico Principal

La inteligencia artificial no realiza cálculos estadísticos.

Todos los cálculos son ejecutados mediante herramientas estadísticas especializadas.

La inteligencia artificial se utiliza exclusivamente para interpretar resultados, generar explicaciones y comprender la intención del usuario.
