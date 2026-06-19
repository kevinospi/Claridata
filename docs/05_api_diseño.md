# Diseño Inicial de la API

## Aprender Estadística

POST /learn/question

Descripción:

Recibe una pregunta relacionada con estadística o probabilidad y devuelve una explicación en lenguaje natural.

## Subida de Dataset

POST /analysis/upload

Descripción:

Recibe un archivo CSV o Excel para su procesamiento.

## Estadísticas Descriptivas

GET /analysis/statistics

Descripción:

Devuelve estadísticas descriptivas del dataset cargado.

## Visualizaciones

GET /analysis/charts

Descripción:

Devuelve las visualizaciones generadas para el dataset.

POST /analysis/charts/custom

Descripción:

Permite solicitar visualizaciones específicas.

## Interpretación

POST /analysis/interpret

Descripción:

Genera una explicación en lenguaje natural sobre los resultados obtenidos.
