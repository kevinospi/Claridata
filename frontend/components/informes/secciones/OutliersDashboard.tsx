"use client";

import { motion } from "framer-motion";
import { InformeDetalleRespuesta } from "@/tipos/api";

interface PropiedadesOutliersDashboard {
  informe: InformeDetalleRespuesta;
}

export function OutliersDashboard({ informe }: PropiedadesOutliersDashboard) {
  const columnas = (informe.deteccion_outliers as any)?.columnas ?? [];
  const conOutliers = columnas.filter((c: any) => c.cantidad_outliers > 0);

  if (!conOutliers.length) {
    return (
      <div className="flex flex-col items-center gap-3 py-8 text-center">
        <span className="text-4xl">✅</span>
        <p className="text-sm font-medium text-claridata-texto">
          No se detectaron valores atípicos
        </p>
        <p className="text-sm text-claridata-textoSecundario">
          Todas las variables están dentro de los límites IQR.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {conOutliers.map((col: any, i: number) => {
        const total = columnas.reduce(
          (acc: number, c: any) => acc + (c.cantidad_outliers ?? 0),
          0,
        );
        const pct =
          informe.estadisticas_descriptivas?.metadatos?.numero_filas
            ? ((col.cantidad_outliers /
                informe.estadisticas_descriptivas.metadatos.numero_filas) *
                100).toFixed(1)
            : "—";

        const severidadColor =
          col.cantidad_outliers >= 5
            ? "#F59E0B"
            : "#67E8F9";

        return (
          <motion.div
            key={col.columna}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: i * 0.05 }}
            className="flex flex-col gap-3 rounded-xl border border-white/10 bg-white/[0.02] px-5 py-4"
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-semibold text-claridata-texto">
                  {col.columna}
                </p>
                <p className="text-xs text-claridata-textoSecundario">
                  {col.cantidad_outliers} valor{col.cantidad_outliers !== 1 ? "es" : ""} atípico{col.cantidad_outliers !== 1 ? "s" : ""} ({pct}% de registros)
                </p>
              </div>
              <span
                className="text-xl font-extrabold"
                style={{ color: severidadColor }}
              >
                {col.cantidad_outliers}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2 text-center">
              {[
                { etiqueta: "Q1", valor: col.q1?.toFixed(2) ?? "—" },
                { etiqueta: "Q3", valor: col.q3?.toFixed(2) ?? "—" },
                { etiqueta: "IQR", valor: col.iqr?.toFixed(2) ?? "—" },
                { etiqueta: "Límite inf.", valor: col.limite_inferior?.toFixed(2) ?? "—" },
                { etiqueta: "Límite sup.", valor: col.limite_superior?.toFixed(2) ?? "—" },
              ].map((item) => (
                <div
                  key={item.etiqueta}
                  className="rounded-lg border border-white/8 bg-white/[0.02] px-2 py-2"
                >
                  <p className="text-xs text-claridata-textoSecundario">{item.etiqueta}</p>
                  <p className="text-sm font-semibold text-claridata-texto">{item.valor}</p>
                </div>
              ))}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}  