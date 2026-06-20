# Diseño de Base de Datos

## Objetivo

Definir la estructura de persistencia de Claridata para el MVP utilizando SQLite, manteniendo compatibilidad futura con PostgreSQL.

La base de datos almacenará usuarios, datasets, informes, conversaciones y mensajes asociados.

---

# Principios de Diseño

* Persistencia opcional de informes.
* Un dataset genera un único informe.
* Una conversación pertenece a un único informe.
* La IA no almacena cálculos; únicamente se almacenan resultados generados.
* Eliminación en cascada para evitar inconsistencias.
* Todas las entidades incluyen auditoría básica.

---

# Entidades

## Usuario

Representa una persona registrada en la plataforma.

### Campos

* id
* nombre
* email
* password_hash
* foto_perfil
* proveedor_autenticacion
* google_id
* fecha_creacion
* fecha_actualizacion

### Relaciones

* Un usuario puede tener múltiples datasets.
* Un usuario puede tener múltiples informes.
* Un usuario puede tener múltiples conversaciones.

---

## Dataset

Representa un archivo cargado por el usuario.

### Campos

* id
* usuario_id
* nombre_archivo
* tipo_archivo (csv/xlsx)
* ruta_archivo
* tamaño_archivo
* numero_filas
* numero_columnas
* columnas
* tipos_datos
* fecha_creacion
* fecha_actualizacion

### Relaciones

* Pertenece a un usuario.
* Genera un único informe.

---

## Informe

Representa el resultado completo del análisis estadístico.

### Campos

* id

* usuario_id

* dataset_id

* resumen_ejecutivo

* estadisticas_descriptivas

* analisis_distribucion

* correlaciones

* deteccion_outliers

* hallazgos_principales

* conclusiones

* fecha_creacion

* fecha_actualizacion

### Relaciones

* Pertenece a un usuario.
* Pertenece a un dataset.
* Puede tener una conversación asociada.

---

## Grafica

Representa una visualización generada automáticamente.

### Campos

* id

* informe_id

* tipo_grafica

* titulo

* ruta_imagen

* fecha_creacion

* fecha_actualizacion

### Relaciones

* Pertenece a un informe.

### Tipos iniciales

* Histograma
* Boxplot
* Gráfico de barras
* Heatmap de correlación
* Scatter plot (cuando aplique)

---

## Conversacion

Representa la memoria contextual asociada a un informe.

### Campos

* id

* usuario_id

* informe_id

* fecha_creacion

* fecha_actualizacion

### Relaciones

* Pertenece a un usuario.
* Pertenece a un informe.
* Contiene múltiples mensajes.

---

## Mensaje

Representa una interacción dentro de una conversación.

### Campos

* id

* conversacion_id

* rol

* contenido

* tipo_respuesta

* fecha_creacion

* fecha_actualizacion

### Valores posibles

#### rol

* usuario
* asistente

#### tipo_respuesta

* corta
* detallada

### Relaciones

* Pertenece a una conversación.

---

# Reglas de Negocio

## Dataset

* Solo se aceptan archivos CSV y XLSX.
* Cada dataset genera un único informe.

---

## Informe

* Se genera automáticamente después del procesamiento del dataset.
* No se guarda automáticamente.
* El usuario decide si desea conservarlo.

---

## Conversación

* Existe únicamente dentro del contexto de un informe.
* Si el informe se guarda, la conversación también se guarda.
* Si el informe se elimina, la conversación también se elimina.

---

## Eliminación en Cascada

Al eliminar un dataset se eliminarán automáticamente:

* Informe asociado
* Gráficas asociadas
* Conversación asociada
* Mensajes asociados

Esto evita inconsistencias y registros huérfanos.

---

# Compatibilidad Futura

La estructura debe diseñarse para permitir una migración sencilla desde SQLite hacia PostgreSQL utilizando SQLAlchemy y Alembic.
