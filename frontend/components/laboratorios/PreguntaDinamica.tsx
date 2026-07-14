"use client";

import { useEffect, useState } from "react";
import {
  EstadoNarrativo,
  MomentoNarrativo,
  obtenerNarrativa,
} from "@/lib/laboratorios/narrativa";

interface PropiedadesPreguntaDinamica {
  momento: MomentoNarrativo;
}

export function PreguntaDinamica({ momento }: PropiedadesPreguntaDinamica) {
  const [narrativa, setNarrativa] = useState<EstadoNarrativo>(
    obtenerNarrativa(momento),
  );
  const [opcionSeleccionada, setOpcionSeleccionada] = useState<string | null>(
    null,
  );
  const [visible, setVisible] = useState(true);
  const [momentoAnterior, setMomentoAnterior] = useState<MomentoNarrativo>(momento);

  useEffect(() => {
    if (momento === momentoAnterior) return;

    setVisible(false);

    const id = setTimeout(() => {
      setNarrativa(obtenerNarrativa(momento));
      setOpcionSeleccionada(null);
      setMomentoAnterior(momento);
      setVisible(true);
    }, 350);

    return () => clearTimeout(id);
  }, [momento, momentoAnterior]);

  return (
    <div
      className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-white/[0.02] px-6 py-6"
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0)" : "translateY(6px)",
        transition: "opacity 350ms ease-out, transform 350ms ease-out",
      }}
    >
      <div className="flex items-start gap-3">
        <span className="text-xl">💬</span>
        <p className="text-base font-medium text-claridata-texto leading-relaxed">
          {narrativa.pregunta}
        </p>
      </div>

      <div className="flex flex-col gap-2">
        {narrativa.opciones.map((opcion) => {
          const seleccionada = opcionSeleccionada === opcion.id;
          return (
            <button
              key={opcion.id}
              type="button"
              onClick={() => setOpcionSeleccionada(opcion.id)}
              className="rounded-xl border px-4 py-3 text-left text-sm transition-all duration-200"
              style={{
                borderColor: seleccionada
                  ? "rgba(34, 211, 238, 0.6)"
                  : "rgba(255,255,255,0.1)",
                backgroundColor: seleccionada
                  ? "rgba(34, 211, 238, 0.08)"
                  : "transparent",
                color: seleccionada ? "#E5E7EB" : "#94A3B8",
              }}
            >
              {opcion.texto}
            </button>
          );
        })}
      </div>

      {opcionSeleccionada && (
        <p
          className="text-sm text-claridata-textoSecundario italic"
          style={{ animation: "aparicion-suave 400ms ease-out forwards" }}
        >
          Sigue explorando — la respuesta está en los datos.
        </p>
      )}
    </div>
  );
}