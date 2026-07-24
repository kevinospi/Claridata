"use client";

import { motion } from "framer-motion";
import { InformeDetalleRespuesta } from "@/tipos/api";

interface PropiedadesResumenEjecutivo {
  informe: InformeDetalleRespuesta;
}

export function ResumenEjecutivo({ informe }: PropiedadesResumenEjecutivo) {
  const metadatos = informe.estadisticas_descriptivas?.metadatos;
  const clasificacion = informe.estadisticas_descriptivas?.clasificacion_variables;
  const nDescubrimientos = informe.descubrimientos?.length ?? 0;
  const nRecomendaciones = informe.recomendaciones_inteligentes?.length ?? 0;

  const resumenAutomatico = metadatos
    ? `Este informe analiza un dataset con ${metadatos.numero_filas.toLocaleString("es-CO")} registros y ${metadatos.numero_columnas} variables ` +
      `(${clasificacion?.numericas?.length ?? 0} numéricas, ${clasificacion?.categoricas?.length ?? 0} categóricas). ` +
      (nDescubrimientos > 0
        ? `El análisis automático identificó ${nDescubrimientos} descubrimiento(s) relevante(s). `
        : "No se detectaron patrones especiales en los datos. ") +
      (nRecomendaciones > 0
        ? `Se generaron ${nRecomendaciones} recomendación(es) para orientar el análisis posterior.`
        : "")
    : "Resumen no disponible.";

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-white/[0.02] px-6 py-6"
    >
      <h3 className="text-sm font-semibold text-claridata-marca uppercase tracking-widest">
        Resumen ejecutivo
      </h3>

      <p className="text-base leading-relaxed text-claridata-textoSecundario">
        {resumenAutomatico}
      </p>
    </motion.div>
  );
}