"use client";

import { motion } from "framer-motion";
import { InformeDetalleRespuesta } from "@/tipos/api";

interface PropiedadesEstadisticasDescriptivas {
  informe: InformeDetalleRespuesta;
}

function formatearNumero(n: number): string {
  if (Math.abs(n) >= 1000) return n.toLocaleString("es-CO", { maximumFractionDigits: 2 });
  return n.toFixed(4).replace(/\.?0+$/, "");
}

export function EstadisticasDescriptivas({ informe }: PropiedadesEstadisticasDescriptivas) {
  const columnas = informe.estadisticas_descriptivas?.columnas ?? [];

  if (!columnas.length) {
    return (
      <p className="text-sm text-claridata-textoSecundario">
        No hay estadísticas descriptivas disponibles.
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      {columnas.map((col: any, i: number) => (
        <motion.div
          key={col.columna}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: i * 0.06 }}
          className="flex flex-col gap-3"
        >
          <div className="flex items-center gap-3">
            <h4 className="text-sm font-semibold text-claridata-texto">{col.columna}</h4>
            <div className="h-px flex-1 bg-white/8" />
          </div>

          <div className="grid grid-cols-3 gap-2 md:grid-cols-6">
            {[
              { etiqueta: "Media", valor: formatearNumero(col.media) },
              { etiqueta: "Mediana", valor: formatearNumero(col.mediana) },
              { etiqueta: "Desv. std.", valor: formatearNumero(col.desviacion_estandar) },
              { etiqueta: "Mínimo", valor: formatearNumero(col.minimo) },
              { etiqueta: "Máximo", valor: formatearNumero(col.maximo) },
              {
                etiqueta: "CV",
                valor: col.media !== 0
                  ? `${((col.desviacion_estandar / Math.abs(col.media)) * 100).toFixed(1)}%`
                  : "—",
              },
            ].map((item) => (
              <div
                key={item.etiqueta}
                className="flex flex-col gap-1 rounded-xl border border-white/8 bg-white/[0.02] px-3 py-3"
              >
                <p className="text-xs text-claridata-textoSecundario">{item.etiqueta}</p>
                <p className="text-base font-semibold text-claridata-texto">{item.valor}</p>
              </div>
            ))}
          </div>
        </motion.div>
      ))}
    </div>
  );
}