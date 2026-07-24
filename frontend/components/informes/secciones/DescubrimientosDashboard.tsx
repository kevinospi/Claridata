"use client";

import { motion } from "framer-motion";
import { DescubrimientoRespuesta, SeveridadDescubrimiento } from "@/tipos/api";

const CONFIG: Record<SeveridadDescubrimiento, {
  emoji: string;
  colorBorde: string;
  colorFondo: string;
  colorTexto: string;
  etiqueta: string;
}> = {
  INFORMATIVO: {
    emoji: "🔵",
    colorBorde: "rgba(59,130,246,0.3)",
    colorFondo: "rgba(59,130,246,0.05)",
    colorTexto: "#93C5FD",
    etiqueta: "Informativo",
  },
  ATENCION: {
    emoji: "🟡",
    colorBorde: "rgba(234,179,8,0.3)",
    colorFondo: "rgba(234,179,8,0.05)",
    colorTexto: "#FDE047",
    etiqueta: "Atención",
  },
  IMPORTANTE: {
    emoji: "🟠",
    colorBorde: "rgba(249,115,22,0.3)",
    colorFondo: "rgba(249,115,22,0.05)",
    colorTexto: "#FDBA74",
    etiqueta: "Importante",
  },
  CRITICO: {
    emoji: "🔴",
    colorBorde: "rgba(239,68,68,0.3)",
    colorFondo: "rgba(239,68,68,0.05)",
    colorTexto: "#FCA5A5",
    etiqueta: "Crítico",
  },
};

const ORDEN: SeveridadDescubrimiento[] = ["CRITICO", "IMPORTANTE", "ATENCION", "INFORMATIVO"];

interface PropiedadesDescubrimientosDashboard {
  descubrimientos: DescubrimientoRespuesta[];
}

export function DescubrimientosDashboard({
  descubrimientos,
}: PropiedadesDescubrimientosDashboard) {
  if (!descubrimientos.length) {
    return (
      <p className="text-sm text-claridata-textoSecundario">
        No se detectaron patrones especiales en este dataset.
      </p>
    );
  }

  const ordenados = [...descubrimientos].sort(
    (a, b) => ORDEN.indexOf(a.severidad) - ORDEN.indexOf(b.severidad),
  );

  const conteo = ORDEN.reduce<Record<string, number>>((acc, s) => {
    acc[s] = descubrimientos.filter((d) => d.severidad === s).length;
    return acc;
  }, {});

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap gap-2">
        {ORDEN.filter((s) => conteo[s] > 0).map((s) => (
          <span
            key={s}
            className="rounded-full px-3 py-1 text-xs font-medium"
            style={{
              color: CONFIG[s].colorTexto,
              backgroundColor: CONFIG[s].colorFondo,
              border: `1px solid ${CONFIG[s].colorBorde}`,
            }}
          >
            {CONFIG[s].emoji} {CONFIG[s].etiqueta}: {conteo[s]}
          </span>
        ))}
      </div>

      <div className="flex flex-col gap-3">
        {ordenados.map((d, i) => {
          const c = CONFIG[d.severidad];
          return (
            <motion.div
              key={`${d.tipo}-${i}`}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: i * 0.04 }}
              className="flex flex-col gap-2 rounded-xl border px-5 py-4"
              style={{ borderColor: c.colorBorde, backgroundColor: c.colorFondo }}
            >
              <div className="flex items-start gap-2">
                <span className="text-sm leading-snug">{c.emoji}</span>
                <div className="flex flex-col gap-0.5">
                  <p className="text-sm font-semibold leading-snug" style={{ color: c.colorTexto }}>
                    {d.titulo}
                  </p>
                  {d.columna && (
                    <p className="text-xs text-claridata-textoSecundario">
                      Variable: <span className="font-mono">{d.columna}</span>
                    </p>
                  )}
                </div>
              </div>
              <p className="text-sm leading-relaxed text-claridata-textoSecundario">{d.descripcion}</p>
              {d.recomendacion && (
                <p className="border-t border-white/5 pt-2 text-xs leading-relaxed text-claridata-textoSecundario">
                  💡 {d.recomendacion}
                </p>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}