import json

from infraestructura.ia.cliente_openai import ClienteOpenAI
from infraestructura.ia.dto_conversacion import ContextoInforme, RespuestaConversacional
from infraestructura.ia.interfaz_interpretador_conversacional import (
    InterpretadorConversacional,
)
from aplicacion.excepciones import ErrorProveedorIA

_PROMPT_SISTEMA = (
    "Eres un analista de datos senior que conversa con un usuario sobre un informe estadístico "
    "ya generado por Claridata. Los cálculos estadísticos ya fueron realizados por Claridata. "
    "No inventes nuevos cálculos ni modifiques resultados. Tu única función es interpretar y "
    "explicar, en español, los datos que se te proporcionan, manteniendo coherencia con el "
    "historial de la conversación. Responde EXCLUSIVAMENTE en formato JSON válido, sin texto "
    "adicional, con esta estructura exacta:\n"
    "{\n"
    '  "contenido": "string",\n'
    '  "tipo_respuesta": "estandar"\n'
    "}"
)


class InterpretadorConversacionalOpenAI(InterpretadorConversacional):
    def __init__(self, cliente_openai: ClienteOpenAI | None = None) -> None:
        self._cliente_openai = cliente_openai or ClienteOpenAI()

    def responder(
        self,
        contexto: ContextoInforme,
        mensaje_usuario: str,
    ) -> RespuestaConversacional:
        mensajes = self._construir_mensajes(contexto, mensaje_usuario)

        contenido_respuesta = self._cliente_openai.completar_chat(mensajes=mensajes)

        return self._parsear_respuesta(contenido_respuesta)

    def _construir_mensajes(
        self,
        contexto: ContextoInforme,
        mensaje_usuario: str,
    ) -> list[dict]:
        contexto_informe_texto = (
            "CONTEXTO DEL INFORME (generado previamente por Claridata, no lo recalcules):\n\n"
            f"Resumen ejecutivo:\n{contexto.resumen_ejecutivo or 'No disponible.'}\n\n"
            f"Conclusiones:\n{contexto.conclusiones or 'No disponible.'}\n\n"
            f"Hallazgos principales:\n"
            f"{json.dumps(contexto.hallazgos_principales, ensure_ascii=False, indent=2)}\n\n"
            f"Recomendaciones:\n"
            f"{json.dumps(contexto.recomendaciones, ensure_ascii=False, indent=2)}\n\n"
            f"Correlaciones:\n"
            f"{json.dumps(contexto.correlaciones, ensure_ascii=False, indent=2)}\n\n"
            f"Detección de outliers:\n"
            f"{json.dumps(contexto.deteccion_outliers, ensure_ascii=False, indent=2)}\n\n"
            f"Análisis de distribución:\n"
            f"{json.dumps(contexto.analisis_distribucion, ensure_ascii=False, indent=2)}\n\n"
            "Recuerda: los cálculos estadísticos ya fueron realizados por Claridata. "
            "No inventes nuevos cálculos ni modifiques resultados. Responde únicamente con el "
            "JSON solicitado, sin explicaciones adicionales fuera de ese formato."
        )

        mensajes: list[dict] = [
            {"role": "system", "content": _PROMPT_SISTEMA},
            {"role": "system", "content": contexto_informe_texto},
        ]

        for mensaje_historial in contexto.historial:
            rol_openai = "assistant" if mensaje_historial.rol == "asistente" else "user"
            mensajes.append({"role": rol_openai, "content": mensaje_historial.contenido})

        mensajes.append({"role": "user", "content": mensaje_usuario})

        return mensajes

    def _parsear_respuesta(self, contenido_respuesta: str) -> RespuestaConversacional:
        try:
            datos = json.loads(contenido_respuesta)
        except json.JSONDecodeError as error:
            raise ErrorProveedorIA(
                "El proveedor de IA devolvió una respuesta que no es JSON válido."
            ) from error

        contenido = datos.get("contenido")
        if not contenido or not isinstance(contenido, str):
            raise ErrorProveedorIA(
                "La respuesta del proveedor de IA no contiene un campo 'contenido' válido."
            )

        tipo_respuesta = datos.get("tipo_respuesta", "estandar")
        if not isinstance(tipo_respuesta, str):
            tipo_respuesta = "estandar"

        return RespuestaConversacional(contenido=contenido, tipo_respuesta=tipo_respuesta)