# Decisiones Arquitectónicas Finales - Claridata

## Estado del Documento

Este documento representa la fuente de verdad arquitectónica definitiva para el MVP de Claridata.

En caso de conflicto entre documentos, este documento tiene prioridad.

---

# Identidad del Producto

## Nombre

Claridata

## Descripción

Claridata es una plataforma de análisis estadístico asistida por inteligencia artificial.

Su objetivo es transformar datos en conocimiento comprensible mediante análisis automáticos, visualizaciones e interpretación en lenguaje natural.

---

# Prioridad del Producto

Claridata es principalmente una herramienta de análisis de datos.

Distribución de enfoque:

- 80% análisis de datos
- 20% educación

La funcionalidad educativa existe para ayudar a comprender los análisis y conceptos estadísticos.

No es una plataforma educativa tradicional.

---

# Filosofía Fundamental

La IA NO realiza cálculos estadísticos.

La IA únicamente:

- Interpreta resultados
- Explica conceptos
- Recomienda análisis
- Responde preguntas
- Enseña estadística

Todos los cálculos deben ser realizados exclusivamente por:

- Pandas
- NumPy
- SciPy
- Statsmodels

---

# MVP

El MVP debe permitir:

- Registro de usuarios
- Inicio de sesión
- Inicio de sesión con Google
- Carga de datasets CSV
- Carga de datasets XLSX
- Generación automática de informes
- Conversación contextual sobre informes
- Tutor estadístico
- Exportación PDF
- Persistencia de informes

---

# Flujo Principal

Dataset

↓

Motor Estadístico

↓

Informe

↓

Interpretación IA

↓

Conversación

↓

Aprendizaje

---

# Dataset

Formatos permitidos:

- CSV
- XLSX

Tamaño máximo inicial:

- 250 MB

Cada dataset genera:

- Un único informe

---

# Informe

El informe debe contener:

## Resumen Ejecutivo

Descripción general de los hallazgos.

## Estadísticas Descriptivas

Resultados fundamentales.

## Distribuciones

Análisis de comportamiento de variables.

## Correlaciones

Relaciones entre variables.

## Detección de Outliers

Valores atípicos relevantes.

## Hallazgos Principales

Aspectos importantes detectados automáticamente.

## Recomendaciones

Sugerencias para profundizar el análisis.

## Conclusiones

Síntesis final.

---

# Visualizaciones

Visualizaciones automáticas:

- Histograma
- Boxplot
- Gráfico de barras
- Heatmap de correlación

Visualizaciones opcionales:

- Scatter Plot
- Otras solicitadas por el usuario

La IA debe reconocer sinónimos.

Ejemplos:

- gráfico de torta → diagrama circular
- caja y bigotes → boxplot
- gráfico de dispersión → scatter plot

---

# Conversaciones

Existen dos tipos de conversación.

## Conversación de Informe

Asociada a:

- Usuario
- Dataset
- Informe

Objetivo:

Permitir preguntas sobre análisis ya realizados.

---

## Conversación de Aprendizaje

Asociada únicamente a:

- Usuario

No requiere dataset.

Objetivo:

Permitir consultas libres de estadística y probabilidad.

---

# Modos de Respuesta

## Corta

Para usuarios con experiencia.

## Estándar

Modo predeterminado.

## Detallada

Para usuarios principiantes.

---

# Comportamiento de la IA

La IA debe comportarse como:

- Analista
- Profesor
- Mentor

Debe ser:

- Profesional
- Cercana
- Paciente
- Didáctica

No debe ser:

- Infantil
- Arrogante
- Sarcástica

---

# Personalidad

La IA debe sentirse como un compañero universitario altamente competente.

Debe adaptar la profundidad de las respuestas al conocimiento demostrado por el usuario.

---

# Memoria Conversacional

Las conversaciones deben conservar:

- Historial completo
- Contexto del informe
- Contexto estadístico relevante

Nunca debe mezclarse información entre informes distintos.

---

# Persistencia

Los informes NO se guardan automáticamente.

El usuario decide si desea guardarlos.

Si un informe se guarda:

- Se guarda la conversación asociada.

Si un informe se elimina:

- Se elimina la conversación asociada.

---

# Base de Datos

MVP:

- SQLite

Escalabilidad futura:

- PostgreSQL

La estructura debe diseñarse utilizando SQLAlchemy para facilitar migraciones futuras.

---

# Backend

Tecnologías:

- Python
- FastAPI

Arquitectura:

- Presentación
- Aplicación
- Dominio
- Infraestructura

Clean Architecture simplificada.

---

# Frontend

Tecnologías:

- React
- TypeScript

Tema:

- Oscuro obligatorio

Colores principales:

- Azul
- Verde

La experiencia debe sentirse moderna y profesional.

No debe parecer una plataforma educativa tradicional.

---

# Visualización del Informe

El informe debe mostrarse dentro de la conversación.

No debe abrir una página independiente.

La experiencia debe sentirse similar a una conversación moderna asistida por IA.

---

# Exportación PDF

El PDF debe contener:

- Resumen ejecutivo
- Estadísticas descriptivas
- Gráficas
- Hallazgos
- Recomendaciones
- Conclusiones

---

# Escalabilidad Futura

Preparar la arquitectura para:

- PostgreSQL
- Streaming estilo ChatGPT
- Procesamiento asíncrono
- Múltiples proveedores de IA
- Compartición de informes
- Multiusuario avanzado

---

# Regla de Desarrollo

El desarrollador NO debe tomar decisiones arquitectónicas adicionales.

Si surge una ambigüedad:

- Mantener la solución más simple.
- Mantener compatibilidad futura.
- Respetar este documento como fuente principal.