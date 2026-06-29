"use client";

import { useEffect, useState } from "react";

const MENSAJES_CARGA = [
  "Preparando el archivo...",
  "Detectando columnas...",
  "Calculando estadísticas...",
  "Generando interpretación...",
];

const DURACION_TOTAL_MS = 2800;
const DURACION_POR_MENSAJE_MS = DURACION_TOTAL_MS / MENSAJES_CARGA.length;

interface PropiedadesPantallaCargaAnalisis {
  alFinalizar: () => void;
}

export function PantallaCargaAnalisis({
  alFinalizar,
}: PropiedadesPantallaCargaAnalisis) {
  const [indiceMensaje, setIndiceMensaje] = useState(0);

  useEffect(() => {
    const intervalo = window.setInterval(() => {
      setIndiceMensaje((indiceActual) =>
        Math.min(indiceActual + 1, MENSAJES_CARGA.length - 1),
      );
    }, DURACION_POR_MENSAJE_MS);

    const temporizadorFinal = window.setTimeout(() => {
      alFinalizar();
    }, DURACION_TOTAL_MS);

    return () => {
      window.clearInterval(intervalo);
      window.clearTimeout(temporizadorFinal);
    };
  }, [alFinalizar]);

  return (
    <div className="flex flex-col items-center justify-center gap-8 py-24 text-center">
      <div className="relative h-16 w-16">
        <div className="absolute inset-0 rounded-full border-4 border-white/10" />
        <div className="absolute inset-0 animate-spin rounded-full border-4 border-transparent border-t-claridata-marca" />
      </div>

      <p className="text-lg font-medium text-claridata-texto">
        Claridata está preparando el análisis...
      </p>

      <p
        key={indiceMensaje}
        className="text-claridata-textoSecundario opacity-0"
        style={{ animation: "aparicion-suave 400ms ease-out 0ms forwards" }}
      >
        {MENSAJES_CARGA[indiceMensaje]}
      </p>
    </div>
  );
}