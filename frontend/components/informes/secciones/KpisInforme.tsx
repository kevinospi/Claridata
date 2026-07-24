"use client";

import { motion } from "framer-motion";
import { InformeDetalleRespuesta } from "@/tipos/api";

interface KpiItem {
  etiqueta: string;
  valor: string;
  subtexto?: string;
  acento: string;
}

interface PropiedadesKpisInforme {
  informe: InformeDetalleRespuesta;
}

function calcularPorcentajeNulos(informe: InformeDetalleRespuesta): string {
  const valoresNulos = informe.estadisticas_descriptivas?.valores_nulos;
  const metadatos = informe.estadisticas_descriptivas?.metadatos;

  if (!valoresNulos || !metadatos) return "—";
  const totalCeldas = metadatos.numero_filas * metadatos.numero_columnas;
  if (totalCeldas === 0) return "0%";

  const pct = (valoresNulos.total / totalCeldas) * 100;
  return `${pct.toFixed(1)}%`;
}

export function KpisInforme({ informe }: PropiedadesKpisInforme) {
  const metadatos = informe.estadisticas_descriptivas?.metadatos;
  const outliersTotales =
    (informe.deteccion_outliers as any)?.columnas?.reduce(
      (acc: number, col: any) => acc + (col.cantidad_outliers ?? 0),
      0,
    ) ?? 0;

  const pares_correlacion =
    (informe.correlaciones as any)?.pares_relevantes?.length ?? 0;

  const kpis: KpiItem[] = [
    {
      etiqueta: "Variables",
      valor: metadatos?.numero_columnas.toString() ?? "—",
      subtexto: `${metadatos?.numero_filas.toLocaleString("es-CO") ?? 0} registros`,
      acento: "#22D3EE",
    },
    {
      etiqueta: "Correlaciones",
      valor: pares_correlacion.toString(),
      subtexto: pares_correlacion > 0 ? "pares relevantes" : "sin relaciones fuertes",
      acento: "#A78BFA",
    },
    {
      etiqueta: "Outliers",
      valor: outliersTotales.toString(),
      subtexto: outliersTotales > 0 ? "valores atípicos" : "dataset limpio",
      acento: outliersTotales > 0 ? "#F59E0B" : "#10B981",
    },
    {
      etiqueta: "Faltantes",
      valor: calcularPorcentajeNulos(informe),
      subtexto: "de completitud total",
      acento:
        parseFloat(calcularPorcentajeNulos(informe)) > 5 ? "#EF4444" : "#10B981",
    },
  ];

  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
      {kpis.map((kpi, i) => (
        <motion.div
          key={kpi.etiqueta}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            duration: 0.4,
            delay: i * 0.07,
            ease: [0.16, 1, 0.3, 1],
          }}
          className="flex flex-col gap-2 rounded-2xl border border-white/10 bg-white/[0.03] px-5 py-5"
          style={{ borderTopColor: kpi.acento, borderTopWidth: 2 }}
        >
          <p className="text-xs font-medium text-claridata-textoSecundario">
            {kpi.etiqueta}
          </p>
          <p
            className="text-3xl font-extrabold tracking-tight"
            style={{ color: kpi.acento }}
          >
            {kpi.valor}
          </p>
          {kpi.subtexto && (
            <p className="text-xs text-claridata-textoSecundario">{kpi.subtexto}</p>
          )}
        </motion.div>
      ))}
    </div>
  );
}