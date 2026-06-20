# Diseño de API

## Objetivo

Definir los endpoints necesarios para el MVP de Claridata.

La API seguirá principios REST y será implementada utilizando FastAPI.

---

# Autenticación

## Registro

### Endpoint

POST /api/v1/auth/registro

### Datos de entrada

* nombre
* email
* password

---

## Inicio de sesión

### Endpoint

POST /api/v1/auth/login

### Respuesta

* access_token
* refresh_token
* token_type

---

## Renovar sesión

### Endpoint

POST /api/v1/auth/refresh

---

## Perfil del usuario

### Endpoint

GET /api/v1/usuarios/me

---
## Inicio de sesión con Google

### Endpoint

POST /api/v1/auth/google

### Datos de entrada

* token_google

### Respuesta

* access_token
* refresh_token
* token_type
---

# Datasets

## Subir dataset

### Endpoint

POST /api/v1/datasets

### Restricciones

* Formato CSV
* Formato XLSX
* Tamaño máximo: 250 MB

---

## Listar datasets

### Endpoint

GET /api/v1/datasets

---

## Obtener dataset

### Endpoint

GET /api/v1/datasets/{dataset_id}

---

## Eliminar dataset

### Endpoint

DELETE /api/v1/datasets/{dataset_id}

---

# Informes

## Generar informe

### Endpoint

POST /api/v1/informes/generar

### Flujo

1. Procesar dataset.
2. Generar estadísticas descriptivas.
3. Analizar distribuciones.
4. Analizar correlaciones.
5. Detectar valores atípicos.
6. Generar visualizaciones.
7. Generar interpretación mediante IA.
8. Generar recomendaciones.
9. Devolver informe completo.

---

## Obtener informe

### Endpoint

GET /api/v1/informes/{informe_id}

---

## Guardar informe

### Endpoint

POST /api/v1/informes/{informe_id}/guardar

---

## Eliminar informe

### Endpoint

DELETE /api/v1/informes/{informe_id}

---

## Exportar PDF

### Endpoint

GET /api/v1/informes/{informe_id}/pdf

### Contenido

* Resumen ejecutivo
* Estadísticas descriptivas
* Gráficas
* Hallazgos principales
* Recomendaciones
* Conclusiones

---

# Conversaciones

## Obtener conversación

### Endpoint

GET /api/v1/conversaciones/{informe_id}

---

## Enviar mensaje

### Endpoint

POST /api/v1/conversaciones/{informe_id}/mensaje

### Datos de entrada

* pregunta
* modo_respuesta

### Modos disponibles

* corta
* estandar
* detallada

---

## Historial de conversación

### Endpoint

GET /api/v1/conversaciones/{informe_id}/historial

---

# Tutor Estadístico

## Consultar concepto

### Endpoint

POST /api/v1/tutor/concepto

---

## Solicitar explicación

### Endpoint

POST /api/v1/tutor/explicacion

---

## Generar ejercicio

### Endpoint

POST /api/v1/tutor/ejercicio

---

## Corregir ejercicio

### Endpoint

POST /api/v1/tutor/corregir

---

# Recomendaciones Inteligentes

Durante la generación del informe, la IA podrá generar automáticamente:

* Recomendaciones de análisis.
* Relaciones potencialmente interesantes.
* Conceptos estadísticos relevantes.
* Sugerencias para profundizar en los datos.

Estas recomendaciones formarán parte del informe generado.

---

# Consideraciones Futuras

## V2

* Streaming tipo ChatGPT.
* Procesamiento asíncrono.
* WebSockets.
* Notificaciones de progreso.
* Compartición de informes.
* Colaboración multiusuario.
