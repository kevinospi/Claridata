"use client";

import { motion } from "framer-motion";
import { InformeDetalleRespuesta } from "@/tipos/api";

interface PropiedadesCorrelacionesDashboard {
  informe: InformeDetalleRespuesta;
}

function colorCorrelacion(r: number): string {
  const abs = Math.abs(r);
  if (abs >= 0.8) return r > 0 ? "#22D3EE" : "#F87171";
  if (abs >= 0.5) return r > 0 ? "#67E8F9" : "#FCA5A5";
  return "#94A3B8";
}

export function CorrelacionesDashboard({ informe }: PropiedadesCorrelacionesDashboard) {
  const pares = (informe.correlaciones as any)?.pares_relevantes ?? [];

  if (!pares.length) {
    return (
      <p className="text-sm text-claridata-textoSecundario">
        No se detectaron correlaciones relevantes en este dataset.
      </p>
    );
  }

  const paresordenados = [...pares].sort(
    (a: any, b: any) => Math.abs(b.coeficiente) - Math.abs(a.coeficiente),
  );

  return (
    <div className="flex flex-col gap-3">
      {paresordenados.map((par: any, i: number) => {
        const color = colorCorrelacion(par.coeficiente);
        const abs = Math.abs(par.coeficiente);
        const intensidad = abs >= 0.8 ? "Muy alta" : abs >= 0.6 ? "Alta" : "Moderada";
        const direccion = par.coeficiente >= 0 ? "positiva" : "negativa";

        return (
          <motion.div
            key={`${par.columna_a}-${par.columna_b}`}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: i * 0.05 }}
            className="flex items-center gap-4 rounded-xl border border-white/10 bg-white/[0.02] px-5 py-4"
          >
            <div className="flex flex-1 flex-col gap-1">
              <p className="text-sm font-semibold text-claridata-texto">
                {par.columna_a}{" "}
                <span className="text-claridata-textoSecundario">↔</span>{" "}
                {par.columna_b}
              </p>
              <p className="text-xs text-claridata-textoSecundario">
                Correlación {intensidad.toLowerCase()} {direccion}
              </p>
            </div>

            <div className="flex flex-col items-end gap-1">
              <span
                className="text-xl font-extrabold tabular-nums"
                style={{ color }}
              >
                {par.coeficiente.toFixed(2)}
              </span>
              <span className="text-xs" style={{ color, opacity: 0.7 }}>
                {intensidad}
              </span>
            </div>

            <div className="h-12 w-1.5 rounded-full bg-white/10">
              <div
                className="rounded-full transition-all"
                style={{
                  height: `${abs * 100}%`,
                  backgroundColor: color,
                  marginTop: `${(1 - abs) * 100}%`,
                }}
              />
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}