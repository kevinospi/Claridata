"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { VisualizacionRespuesta, PrioridadVisualizacion } from "@/tipos/api";
import { Histograma } from "./Histograma";
import { BoxPlot } from "./BoxPlot";
import { ScatterPlot } from "./ScatterPlot";
import { Heatmap } from "./Heatmap";
import { Barras } from "./Barras";

const CONFIG_PRIORIDAD: Record<PrioridadVisualizacion, { etiqueta: string; color: string }> = {
  ALTA: { etiqueta: "Alta", color: "#22D3EE" },
  MEDIA: { etiqueta: "Media", color: "#A78BFA" },
  BAJA: { etiqueta: "Baja", color: "#94A3B8" },
};

interface PropiedadesRenderizadorGraficas {
  visualizaciones: VisualizacionRespuesta[];
}

function renderizarGrafica(visualizacion: VisualizacionRespuesta) {
  switch (visualizacion.tipo) {
    case "HISTOGRAMA":
    case "DISTRIBUCION":
      return <Histograma visualizacion={visualizacion} />;
    case "BOXPLOT":
      return <BoxPlot visualizacion={visualizacion} />;
    case "SCATTER":
      return <ScatterPlot visualizacion={visualizacion} />;
    case "HEATMAP":
      return <Heatmap visualizacion={visualizacion} />;
    case "BARRAS":
      return <Barras visualizacion={visualizacion} />;
    default:
      return (
        <div className="flex h-48 items-center justify-center text-claridata-textoSecundario text-sm">
          Tipo de gráfica no soportado: {visualizacion.tipo}
        </div>
      );
  }
}

function TarjetaVisualizacion({ vis }: { vis: VisualizacionRespuesta }) {
  const [expandida, setExpandida] = useState(true);
  const prioridadCfg = CONFIG_PRIORIDAD[vis.prioridad];

  return (
    <div className="flex flex-col rounded-2xl border border-white/10 bg-white/[0.02] overflow-hidden">
      <button
        type="button"
        onClick={() => setExpandida((v) => !v)}
        className="flex items-center justify-between gap-3 px-5 py-4 text-left transition-colors hover:bg-white/[0.03]"
      >
        <div className="flex items-center gap-3">
          <span
            className="h-2 w-2 rounded-full"
            style={{ backgroundColor: prioridadCfg.color }}
          />
          <div className="flex flex-col gap-0.5">
            <p className="text-sm font-semibold text-claridata-texto">
              {vis.titulo}
            </p>
            <p className="text-xs text-claridata-textoSecundario">
              {vis.descripcion}
            </p>
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-2">
          <span
            className="rounded-full px-2 py-0.5 text-xs font-medium"
            style={{
              color: prioridadCfg.color,
              backgroundColor: `${prioridadCfg.color}15`,
              border: `1px solid ${prioridadCfg.color}30`,
            }}
          >
            {prioridadCfg.etiqueta}
          </span>
          <span className="text-xs text-claridata-textoSecundario">
            {expandida ? "▲" : "▼"}
          </span>
        </div>
      </button>

      <AnimatePresence initial={false}>
        {expandida && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="overflow-hidden border-t border-white/8"
          >
            <div className="px-5 py-4">
              {renderizarGrafica(vis)}
              <p className="mt-2 text-xs text-claridata-textoSecundario">
                💡 {vis.motivo}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export function RenderizadorGraficas({
  visualizaciones,
}: PropiedadesRenderizadorGraficas) {
  const [filtro, setFiltro] = useState<string>("TODAS");

  if (!visualizaciones.length) {
    return (
      <p className="text-sm text-claridata-textoSecundario">
        No se generaron visualizaciones para este informe.
      </p>
    );
  }

  const tipos = ["TODAS", ...new Set(visualizaciones.map((v) => v.tipo))];
  const filtradas =
    filtro === "TODAS"
      ? visualizaciones
      : visualizaciones.filter((v) => v.tipo === filtro);

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap gap-2">
        {tipos.map((tipo) => (
          <button
            key={tipo}
            type="button"
            onClick={() => setFiltro(tipo)}
            className="rounded-full border px-3 py-1 text-xs font-medium transition-colors"
            style={{
              borderColor:
                filtro === tipo
                  ? "rgba(34,211,238,0.5)"
                  : "rgba(255,255,255,0.1)",
              backgroundColor:
                filtro === tipo
                  ? "rgba(34,211,238,0.1)"
                  : "transparent",
              color: filtro === tipo ? "#22D3EE" : "#94A3B8",
            }}
          >
            {tipo}
          </button>
        ))}
      </div>

      <div className="flex flex-col gap-3">
        {filtradas.map((vis, i) => (
          <TarjetaVisualizacion key={`${vis.tipo}-${i}`} vis={vis} />
        ))}
      </div>
    </div>
  );
}