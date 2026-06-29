"use client";

import { DefinicionModo } from "@/tipos/modo";

interface PropiedadesTarjetaModo {
  modo: DefinicionModo;
  estaEnHover: boolean;
  estaExpandiendo: boolean;
  estaDesapareciendo: boolean;
  alIniciarHover: () => void;
  alFinalizarHover: () => void;
  alSeleccionar: () => void;
}

export function TarjetaModo({
  modo,
  estaEnHover,
  estaExpandiendo,
  estaDesapareciendo,
  alIniciarHover,
  alFinalizarHover,
  alSeleccionar,
}: PropiedadesTarjetaModo) {
  const colorTexto = modo.colorAcento === "amarillo" ? "#3F2D03" : "#022C33";
  const colorTextoSecundario =
    modo.colorAcento === "amarillo" ? "#6B4E0A" : "#0A4A52";

  const claseAltura = estaExpandiendo
    ? "flex-grow-[10]"
    : estaDesapareciendo
      ? "flex-grow-0 basis-0 opacity-0"
      : "flex-1";

  return (
    <button
      type="button"
      onMouseEnter={alIniciarHover}
      onMouseLeave={alFinalizarHover}
      onClick={alSeleccionar}
      aria-label={`Entrar a ${modo.titulo}`}
      style={{
        background: `linear-gradient(135deg, ${modo.degradadoDesde}, ${modo.degradadoHasta})`,
        animation: "aparicion-suave 700ms ease-out 750ms forwards",
      }}
      className={`
        group relative flex w-full flex-col
        items-center justify-center overflow-hidden px-6 py-16
        text-center opacity-0
        transition-all duration-700 ease-claridata-expo
        ${claseAltura}
        ${estaEnHover && !estaExpandiendo ? "scale-[1.01] brightness-[1.15]" : "scale-100 brightness-100"}
      `}
    >
      <h2
        style={{ color: colorTexto }}
        className={`
          text-4xl font-bold tracking-tight transition-transform duration-500
          md:text-5xl
          ${estaEnHover && !estaExpandiendo ? "scale-[1.03]" : "scale-100"}
        `}
      >
        {modo.titulo}
      </h2>

      <p
        style={{ color: colorTextoSecundario }}
        className="mt-4 max-w-sm whitespace-pre-line text-base font-medium md:text-lg"
      >
        {modo.descripcion}
      </p>
    </button>
  );
}