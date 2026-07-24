"use client";

import { motion } from "framer-motion";
import { InformeDetalleRespuesta } from "@/tipos/api";

interface PropiedadesHeroInforme {
  informe: InformeDetalleRespuesta;
  alRenombrar?: () => void;
}

function formatearFecha(fechaIso: string): string {
  return new Date(fechaIso).toLocaleString("es-CO", {
    dateStyle: "long",
    timeStyle: "short",
  });
}

export function HeroInforme({ informe, alRenombrar }: PropiedadesHeroInforme) {
  const metadatos = informe.estadisticas_descriptivas?.metadatos;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      className="flex flex-col gap-4 rounded-3xl border border-white/10 bg-gradient-to-br from-white/[0.04] to-transparent px-8 py-8"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex flex-col gap-1">
          <p className="text-xs font-semibold uppercase tracking-widest text-claridata-marca">
            Informe estadístico
          </p>
          <h1 className="text-2xl font-extrabold tracking-tight text-claridata-texto md:text-3xl">
            {informe.titulo}
          </h1>
          <p className="text-sm text-claridata-textoSecundario">
            {formatearFecha(informe.fecha_creacion)}
          </p>
        </div>

        <div className="flex shrink-0 items-center gap-2">
          <span
            className="rounded-full px-3 py-1 text-xs font-semibold"
            style={{
              backgroundColor: informe.guardado
                ? "rgba(34, 211, 238, 0.12)"
                : "rgba(255,255,255,0.06)",
              color: informe.guardado ? "#22D3EE" : "#94A3B8",
              border: `1px solid ${informe.guardado ? "rgba(34,211,238,0.3)" : "rgba(255,255,255,0.1)"}`,
            }}
          >
            {informe.guardado ? "Guardado" : "Analizado"}
          </span>

          {alRenombrar && (
            <button
              type="button"
              onClick={alRenombrar}
              aria-label="Renombrar informe"
              className="rounded-full border border-white/15 p-2 text-claridata-textoSecundario transition-colors hover:border-white/30 hover:text-claridata-texto"
            >
              ✏️
            </button>
          )}
        </div>
      </div>

      {metadatos && (
        <div className="mt-2 grid grid-cols-2 gap-3 border-t border-white/8 pt-4 md:grid-cols-4">
          {[
            { etiqueta: "Registros", valor: metadatos.numero_filas.toLocaleString("es-CO") },
            { etiqueta: "Variables", valor: metadatos.numero_columnas.toString() },
            {
              etiqueta: "Numéricas",
              valor: informe.estadisticas_descriptivas?.clasificacion_variables?.numericas?.length?.toString() ?? "—",
            },
            {
              etiqueta: "Categóricas",
              valor: informe.estadisticas_descriptivas?.clasificacion_variables?.categoricas?.length?.toString() ?? "—",
            },
          ].map((item) => (
            <div key={item.etiqueta} className="flex flex-col gap-0.5">
              <p className="text-xs text-claridata-textoSecundario">{item.etiqueta}</p>
              <p className="text-xl font-bold text-claridata-texto">{item.valor}</p>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  );
}