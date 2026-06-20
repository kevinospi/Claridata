# Arquitectura Backend

## Objetivo

Definir la arquitectura interna del backend de Claridata, sus responsabilidades, componentes y flujo principal de procesamiento.

El backend será implementado utilizando Python y FastAPI siguiendo principios de Clean Architecture simplificada.

---

# Stack Tecnológico

## Backend

* Python
* FastAPI

## Motor Estadístico

* Pandas
* NumPy
* SciPy
* Statsmodels

## Inteligencia Artificial

* OpenAI (MVP)

## Base de Datos

* SQLite (MVP)
* PostgreSQL (futuro)

## Generación PDF

* HTML + PDF

## Visualizaciones

* Plotly (gráficas interactivas)
* Matplotlib (exportación PDF)

---

# Arquitectura General

El backend seguirá una versión simplificada de Clean Architecture.

Estructura principal:

app/

* presentacion/
* aplicacion/
* dominio/
* infraestructura/

---

# Capa de Presentación

Responsabilidad:

Recibir solicitudes HTTP y devolver respuestas al cliente.

Contendrá:

* Endpoints FastAPI
* Validación de solicitudes
* Serialización de respuestas
* Manejo de errores HTTP

No debe contener:

* Reglas de negocio
* Lógica estadística
* Integración directa con IA

---

# Capa de Aplicación

Responsabilidad:

Coordinar los casos de uso del sistema.

Contendrá:

* Casos de uso
* Orquestación de procesos
* Coordinación entre dominio e infraestructura

Organización:

aplicacion/

* usuarios/
* datasets/
* informes/
* conversaciones/
* tutor/

Ejemplos:

* registrar_usuario
* iniciar_sesion
* subir_dataset
* generar_informe
* guardar_informe
* exportar_pdf
* enviar_mensaje

---

# Capa de Dominio

Responsabilidad:

Representar las reglas centrales del negocio.

Contendrá:

* Entidades
* Contratos
* Interfaces
* Reglas de negocio

Ejemplos:

* Usuario
* Dataset
* Informe
* Conversacion
* Mensaje

La capa de dominio no debe depender de ninguna tecnología externa.

---

# Capa de Infraestructura

Responsabilidad:

Implementar los servicios externos utilizados por el sistema.

Contendrá:

* Base de datos
* OpenAI
* Archivos
* PDF
* Visualizaciones

Ejemplos:

* Repositorios
* Cliente OpenAI
* Generador PDF
* Gestor de archivos

---

# Proveedor de IA

Claridata utilizará una capa de abstracción para proveedores de inteligencia artificial.

Objetivo:

Permitir cambiar OpenAI por cualquier otro proveedor sin modificar la lógica de negocio.

Ejemplo conceptual:

ProveedorIA

Implementaciones:

* OpenAIProvider
* AnthropicProvider
* GeminiProvider
* DeepSeekProvider

Inicialmente solo se implementará OpenAI.

---

# Motor Estadístico

Existirá un componente central denominado:

MotorEstadistico

Responsabilidades:

* Analizar datasets
* Generar estadísticas descriptivas
* Analizar distribuciones
* Calcular correlaciones
* Detectar valores atípicos
* Generar resultados estructurados

El motor estadístico será la única fuente autorizada para realizar cálculos.

La IA nunca realizará cálculos estadísticos.

---

# Memoria Conversacional

Cada conversación estará asociada a un único informe.

Cuando el usuario envíe una pregunta, la IA recibirá:

* Pregunta actual
* Historial completo de conversación
* Informe asociado
* Contexto estadístico relevante

Esto permitirá mantener coherencia durante toda la interacción.

---

# Generación de Gráficas

## Plotly

Utilizado para:

* Visualizaciones interactivas
* Exploración de datos
* Experiencia de usuario moderna

## Matplotlib

Utilizado para:

* Exportación PDF
* Generación de imágenes estáticas

---

# Flujo Principal del Sistema

Cuando un usuario carga un dataset:

1. Validar archivo.
2. Leer dataset.
3. Analizar dataset.
4. Generar estadísticas.
5. Generar gráficas.
6. Construir informe técnico.
7. Enviar contexto a la IA.
8. Generar informe interpretado.
9. Generar recomendaciones.
10. Devolver informe completo.

---

# Seguridad

Autenticación:

* JWT Access Token
* JWT Refresh Token

En el MVP no se implementará Rate Limiting.

Podrá añadirse en futuras versiones cuando exista tráfico real.

---

# Principios Arquitectónicos

## Separación de responsabilidades

Cada capa tendrá una única responsabilidad claramente definida.

---

## Desacoplamiento de proveedores

La lógica del negocio no dependerá directamente de OpenAI.

---

## Escalabilidad futura

La arquitectura debe permitir:

* Migrar SQLite a PostgreSQL.
* Cambiar proveedor IA.
* Incorporar procesamiento asíncrono.
* Implementar microservicios si fuera necesario.

---

# Filosofía General

La inteligencia artificial interpreta.

El motor estadístico calcula.

La arquitectura debe garantizar que ambas responsabilidades permanezcan separadas.

---

# Autenticación

Claridata soportará dos métodos de autenticación:

- Email y contraseña
- Google OAuth

Ambos métodos generarán los mismos JWT internos del sistema.

La lógica del negocio no distinguirá el origen de autenticación.