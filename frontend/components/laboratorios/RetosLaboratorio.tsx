"use client";

import { useState } from "react";

interface Reto {
  id: string;
  titulo: string;
  descripcion: string;
}

const RETOS: Reto[] = [
  {
    id: "presupuesto",
    titulo: "El presupuesto del alcalde",
    descripcion:
      "El gobierno dice que el salario promedio es $10M. Mueve los valores para que sea cierto, pero que la mayoría gane mucho menos. ¿Puedes lograrlo?",
  },
  {
    id: "equilibrio",
    titulo: "Equilíbralos",
    descripcion:
      "¿Puedes crear una distribución donde media, mediana y moda sean exactamente el mismo número? Pruébalo.",
  },
  {
    id: "inmune",
    titulo: "La mediana inmune",
    descripcion:
      "Arrastra el valor extremo lo más lejos posible. ¿Puedes hacer que la mediana no cambie en absoluto mientras la media se dispara?",
  },
];

interface PropiedadesRetosLaboratorio {
  retoActivo: string | null;
  alSeleccionarReto: (id: string | null) => void;
}

export function RetosLaboratorio({
  retoActivo,
  alSeleccionarReto,
}: PropiedadesRetosLaboratorio) {
  const [expandido, setExpandido] = useState(false);

  return (
    <div className="flex flex-col gap-3">
      <button
        type="button"
        onClick={() => setExpandido((v) => !v)}
        className="flex items-center justify-between rounded-xl border border-white/10 px-4 py-3 text-left transition-colors hover:border-white/20"
      >
        <span className="text-sm font-medium text-claridata-textoSecundario">
          🎯 Retos opcionales
        </span>
        <span className="text-xs text-claridata-textoSecundario">
          {expandido ? "▲ ocultar" : "▼ ver retos"}
        </span>
      </button>

      {expandido && (
        <div
          className="flex flex-col gap-2"
          style={{ animation: "aparicion-suave 300ms ease-out forwards" }}
        >
          {RETOS.map((reto) => {
            const activo = retoActivo === reto.id;
            return (
              <button
                key={reto.id}
                type="button"
                onClick={() =>
                  alSeleccionarReto(activo ? null : reto.id)
                }
                className="flex flex-col gap-2 rounded-xl border px-4 py-4 text-left transition-all duration-200"
                style={{
                  borderColor: activo
                    ? "rgba(34, 211, 238, 0.5)"
                    : "rgba(255,255,255,0.08)",
                  backgroundColor: activo
                    ? "rgba(34, 211, 238, 0.05)"
                    : "transparent",
                }}
              >
                <span className="text-sm font-semibold text-claridata-texto">
                  {reto.titulo}
                </span>
                <span className="text-sm text-claridata-textoSecundario">
                  {reto.descripcion}
                </span>
                {activo && (
                  <span className="text-xs text-claridata-marca">
                    Reto activo — experimenta en la línea de datos ↑
                  </span>
                )}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}