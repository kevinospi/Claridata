"use client";

import { useState } from "react";
import { EjercicioRespuestaNumerica } from "@/tipos/aprendizaje";
import { RespuestaEjercicio } from "./RespuestaEjercicio";

interface PropiedadesEjercicioInteractivo {
  ejercicio: EjercicioRespuestaNumerica;
}

const TOLERANCIA = 0.01;

export function EjercicioInteractivo({
  ejercicio,
}: PropiedadesEjercicioInteractivo) {
  const [respuestaUsuario, setRespuestaUsuario] = useState("");
  const [enviado, setEnviado] = useState(false);
  const [esCorrecta, setEsCorrecta] = useState(false);

  const manejarComprobar = () => {
    const valorNumerico = Number(respuestaUsuario);

    if (Number.isNaN(valorNumerico)) {
      return;
    }

    const correcta =
      Math.abs(valorNumerico - ejercicio.respuestaCorrecta) < TOLERANCIA;

    setEsCorrecta(correcta);
    setEnviado(true);
  };

  const manejarIntentarDeNuevo = () => {
    setEnviado(false);
    setRespuestaUsuario("");
  };

  return (
    <div className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-white/[0.03] px-6 py-6">
      <p className="font-medium text-claridata-texto">{ejercicio.pregunta}</p>

      <div className="flex flex-wrap gap-2">
        {ejercicio.datos.map((dato, indice) => (
          <span
            key={indice}
            className="rounded-lg bg-white/[0.05] px-3 py-1.5 text-sm text-claridata-textoSecundario"
          >
            {dato}
          </span>
        ))}
      </div>

      {!enviado ? (
        <div className="flex items-center gap-3">
          <input
            type="number"
            value={respuestaUsuario}
            onChange={(evento) => setRespuestaUsuario(evento.target.value)}
            placeholder="Tu respuesta"
            className="w-40 rounded-xl border border-white/15 bg-white/[0.03] px-4 py-2.5 text-claridata-texto outline-none focus:border-claridata-marca"
          />
          <button
            type="button"
            onClick={manejarComprobar}
            disabled={respuestaUsuario.trim() === ""}
            className="rounded-full bg-claridata-marca px-5 py-2.5 text-sm font-semibold text-[#022C33] transition-transform hover:scale-[1.03] disabled:opacity-40"
          >
            Comprobar
          </button>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          <RespuestaEjercicio
            esCorrecta={esCorrecta}
            explicacion={ejercicio.explicacion}
          />
          <button
            type="button"
            onClick={manejarIntentarDeNuevo}
            className="self-start rounded-full border border-white/15 px-4 py-2 text-sm text-claridata-textoSecundario transition-colors hover:border-white/30 hover:text-claridata-texto"
          >
            Intentar de nuevo
          </button>
        </div>
      )}
    </div>
  );
}