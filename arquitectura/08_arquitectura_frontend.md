# Arquitectura Frontend

## Objetivo

Definir la estructura visual, experiencia de usuario y organización general del frontend de Claridata.

El frontend será implementado utilizando React y TypeScript.

La experiencia principal estará inspirada en interfaces conversacionales modernas, priorizando simplicidad, claridad y accesibilidad.

---

# Stack Tecnológico

## Framework

* React

## Lenguaje

* TypeScript

## Comunicación

* API REST (FastAPI)

## Visualizaciones

* Plotly

---

# Filosofía de Diseño

Claridata no debe sentirse como una plataforma estadística tradicional.

El objetivo es que cualquier usuario pueda obtener análisis complejos simplemente conversando con el sistema.

El usuario no debe preocuparse por programar, configurar herramientas ni interpretar código.

La experiencia debe sentirse natural, moderna y profesional.

---

# Identidad Visual

## Tema

* Modo oscuro obligatorio.

## Colores principales

* Azul
* Verde

## Colores secundarios

* Escala de grises oscuros

## Tipografía

* Moderna
* Alta legibilidad
* Apariencia profesional

---

# Principios de Experiencia de Usuario

## Simplicidad

Reducir al mínimo la complejidad visual.

---

## Aprendizaje Guiado

Ayudar al usuario a comprender conceptos sin sentirse abrumado.

---

## Conversación Primero

La interacción principal ocurre mediante conversación.

---

## Datos Primero

Las visualizaciones deben facilitar la comprensión y no convertirse en elementos decorativos.

---

# Pantalla Principal

Al ingresar a Claridata, el usuario visualizará:

* Logo de Claridata
* Mensaje de bienvenida
* Selector de experiencia

Opciones:

## Aprendizaje

Permite conversar libremente con la IA sobre:

* Estadística
* Probabilidad
* Conceptos
* Ejercicios
* Explicaciones

No requiere dataset.

---

## Análisis

Permite iniciar un análisis de datos.

Acciones:

* Arrastrar archivo
* Seleccionar archivo

Formatos permitidos:

* CSV
* XLSX

---

# Experiencia Conversacional

Claridata utilizará una interfaz inspirada en aplicaciones conversacionales modernas.

La conversación será el eje central de la experiencia.

Ejemplo:

Usuario:

* Carga dataset

Claridata:

* Genera informe
* Presenta resultados
* Responde preguntas
* Realiza recomendaciones

---

# Presentación del Informe

El informe aparecerá directamente dentro de la conversación.

No se abrirá una página independiente.

La generación del informe será percibida como una respuesta de Claridata.

---

# Estructura del Informe

## Resumen Ejecutivo

Explicación general de los hallazgos más importantes.

---

## Estadísticas Descriptivas

Resultados fundamentales del análisis.

---

## Visualizaciones

Cada visualización incluirá:

* Gráfica
* Interpretación
* Explicación contextual

Formato:

Gráfica

↓

Interpretación

↓

Explicación

---

## Hallazgos Principales

Aspectos relevantes detectados durante el análisis.

---

## Recomendaciones

Sugerencias generadas por IA para profundizar en el análisis.

---

## Conclusiones

Síntesis final del informe.

---

# Botón "Explícamelo"

Disponible en prácticamente cualquier elemento relevante del informe.

Ejemplos:

* Media
* Mediana
* Moda
* Desviación estándar
* p-valor
* Correlaciones
* Outliers
* Gráficas
* Recomendaciones

Objetivo:

Permitir al usuario comprender cualquier resultado sin abandonar el flujo de trabajo.

---

# Historial de Informes

Existirá una barra lateral similar a aplicaciones conversacionales modernas.

Permitirá acceder a:

* Informes guardados
* Conversaciones asociadas

Ejemplos:

* Informe de Ventas
* Encuesta de Clientes
* Investigación Académica

---

# Conversaciones Persistentes

Cada informe tendrá una conversación asociada.

Al reabrir un informe guardado:

* Se recuperará la conversación completa.
* Se recuperará el informe completo.
* El contexto permanecerá disponible.

---

# Visualizaciones

## Plotly

Se utilizará para:

* Gráficas interactivas
* Zoom
* Exploración de datos
* Mejor experiencia visual

---

# Responsive Design

Claridata será compatible con:

## Escritorio

Experiencia principal.

---

## Dispositivos móviles

Versión optimizada para pantallas pequeñas.

El diseño responsive no debe comprometer rendimiento ni legibilidad.

---

# Navegación

Estructura general:

Inicio

↓

Aprendizaje o Análisis

↓

Conversación

↓

Informe

↓

Profundización

↓

Exportación PDF

---

# Filosofía General

Claridata no es una herramienta estadística tradicional.

Claridata es un analista inteligente que conversa con el usuario, explica resultados y transforma datos complejos en conocimiento comprensible.
