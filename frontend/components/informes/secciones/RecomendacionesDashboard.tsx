"use client";

import { motion } from "framer-motion";
import { PrioridadRecomendacion, RecomendacionRespuesta } from "@/tipos/api";

const CONFIG: Record<PrioridadRecomendacion, {
  etiqueta: string;
  colorTexto: string;
  colorFondo: string;
  colorBorde: string;
}> = {
  ALTA: {
    etiqueta: "Alta",
    colorTexto: "#FCA5A5",
    colorFondo: "rgba(239,68,68,0.08)",
    colorBorde: "rgba(239,68,68,0.25)",
  },
  MEDIA: {
    etiqueta: "Media",
    colorTexto: "#FDE047",
    colorFondo: "rgba(234,179,8,0.08)",
    colorBorde: "rgba(234,179,8,0.25)",
  },
  BAJA: {
    etiqueta: "Baja",
    colorTexto: "#86EFAC",
    colorFondo: "rgba(34,197,94,0.08)",
    colorBorde: "rgba(34,197,94,0.25)",
  },
};

const ORDEN: PrioridadRecomendacion[] = ["ALTA", "MEDIA", "BAJA"];

interface PropiedadesRecomendacionesDashboard {
  recomendaciones: RecomendacionRespuesta[];
}

function TarjetaRecomendacion({ r, delay }: { r: RecomendacionRespuesta; delay: number }) {
  const c = CONFIG[r.prioridad];
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay, ease: [0.16, 1, 0.3, 1] }}
      className="flex flex-col gap-3 rounded-2xl border border-white/10 bg-white/[0.02] px-5 py-5"
    >
      <div className="flex items-start justify-between gap-3">
        <p className="text-sm font-semibold leading-snug text-claridata-texto">
          {r.titulo}
        </p>
        <span
          className="shrink-0 rounded-full px-2.5 py-0.5 text-xs font-medium"
          style={{ color: c.colorTexto, backgroundColor: c.colorFondo, border: `1px solid ${c.colorBorde}` }}
        >
          {c.etiqueta}
        </span>
      </div>

      <p className="text-xs font-medium uppercase tracking-wide" style={{ color: c.colorTexto, opacity: 0.7 }}>
        {r.categoria}
      </p>

      <p className="text-sm leading-relaxed text-claridata-textoSecundario">{r.razon}</p>

      <div className="rounded-xl bg-white/[0.03] px-4 py-3">
        <p className="mb-1 text-xs font-semibold text-claridata-textoSecundario">¿Qué hacer?</p>
        <p className="whitespace-pre-line text-sm leading-relaxed text-claridata-textoSecundario">
          {r.accion}
        </p>
      </div>
    </motion.div>
  );
}

export function RecomendacionesDashboard({
  recomendaciones,
}: PropiedadesRecomendacionesDashboard) {
  if (!recomendaciones.length) {
    return (
      <p className="text-sm text-claridata-textoSecundario">
        No se generaron recomendaciones para este informe.
      </p>
    );
  }

  const agrupadas = ORDEN.reduce<Record<PrioridadRecomendacion, RecomendacionRespuesta[]>>(
    (acc, p) => ({ ...acc, [p]: [] }),
    { ALTA: [], MEDIA: [], BAJA: [] },
  );
  for (const r of recomendaciones) agrupadas[r.prioridad].push(r);

  let delayAcumulado = 0;

  return (
    <div className="flex flex-col gap-6">
      {ORDEN.filter((p) => agrupadas[p].length > 0).map((prioridad) => {
        const c = CONFIG[prioridad];
        return (
          <div key={prioridad} className="flex flex-col gap-3">
            <p
              className="text-xs font-semibold uppercase tracking-widest"
              style={{ color: c.colorTexto, opacity: 0.8 }}
            >
              Prioridad {c.etiqueta}
            </p>
            {agrupadas[prioridad].map((r, i) => {
              const delay = delayAcumulado * 0.05;
              delayAcumulado++;
              return <TarjetaRecomendacion key={`${r.titulo}-${i}`} r={r} delay={delay} />;
            })}
          </div>
        );
      })}
    </div>
  );
}