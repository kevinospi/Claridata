# Modelo de Dominio

## Entidades principales

### Usuario

Representa una persona registrada dentro de la plataforma.

Responsabilidades:

* Gestionar datasets
* Gestionar informes
* Mantener conversaciones
* Resolver ejercicios

---

### Dataset

Representa un archivo cargado por el usuario.

Formatos soportados:

* CSV
* XLSX

Relaciones:

* Pertenece a un usuario
* Genera un único informe

---

### Informe

Representa el resultado generado a partir de un dataset.

Contiene:

* Estadísticas descriptivas
* Distribuciones
* Correlaciones
* Detección de valores atípicos
* Hallazgos automáticos
* Visualizaciones
* Interpretaciones

Relaciones:

* Pertenece a un dataset
* Pertenece a un usuario
* Puede tener una conversación asociada

---

### Conversación

Representa el contexto conversacional asociado a un informe.

Objetivo:

Permitir que el usuario haga preguntas sobre el análisis realizado.

Relaciones:

* Pertenece a un informe
* Contiene múltiples mensajes

---

### Mensaje

Representa una interacción dentro de una conversación.

Tipos:

* Usuario
* Asistente

Modos de respuesta:

* Corta
* Detallada


