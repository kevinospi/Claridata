"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { SeccionInterpretacionRespuesta } from "@/tipos/api";

const ICONO: Record<string, string> = {
  RESUMEN_GENERAL: "📋",
  VARIABLES_DESTACADAS: "📊",
  PATRONES_DETECTADOS: "🔍",
  CALIDAD_DATOS: "🛡️",
  RELACIONES_ENCONTRADAS: "🔗",
  IMPLICACIONES: "⚠️",
  RECOMENDACIONES_ANALITICAS: "💡",
};

interface PropiedadesInterpretacionDashboard {
  secciones: SeccionInterpretacionRespuesta[];
}

function Acordeon({ seccion }: { seccion: SeccionInterpretacionRespuesta }) {
  const [abierto, setAbierto] = useState(false);
  const icono = ICONO[seccion.tipo] ?? "📄";

  return (
    <div className="rounded-xl border border-white/10 overflow-hidden">
      <button
        type="button"
        onClick={() => setAbierto((v) => !v)}
        className="flex w-full items-center justify-between gap-3 bg-white/[0.02] px-5 py-4 text-left transition-colors hover:bg-white/[0.04]"
      >
        <div className="flex items-center gap-3">
          <span className="text-base">{icono}</span>
          <span className="text-sm font-semibold text-claridata-texto">
            {seccion.titulo}
          </span>
          <span className="text-xs text-claridata-textoSecundario">
            {seccion.parrafos.length} párrafo{seccion.parrafos.length !== 1 ? "s" : ""}
          </span>
        </div>
        <span className="text-xs text-claridata-textoSecundario">
          {abierto ? "▲" : "▼"}
        </span>
      </button>

      <AnimatePresence initial={false}>
        {abierto && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="overflow-hidden"
          >
            <div className="flex flex-col gap-3 border-t border-white/8 px-5 py-4">
              {seccion.parrafos.map((p, i) => (
                <p key={i} className="text-sm leading-relaxed text-claridata-textoSecundario">
                  {p}
                </p>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export function InterpretacionDashboard({
  secciones,
}: PropiedadesInterpretacionDashboard) {
  if (!secciones.length) {
    return (
      <p className="text-sm text-claridata-textoSecundario">
        La interpretación profesional no está disponible para este informe.
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {secciones.map((s) => (
        <Acordeon key={s.tipo} seccion={s} />
      ))}
    </div>
  );
}