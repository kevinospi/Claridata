"use client";

import { DefinicionModo } from "@/tipos/modo";

interface PropiedadesTarjetaModo {
  modo: DefinicionModo;
  estaEnHover: boolean;
  alIniciarHover: () => void;
  alFinalizarHover: () => void;
  alSeleccionar: () => void;
}

export function TarjetaModo({
  modo,
  estaEnHover,
  alIniciarHover,
  alFinalizarHover,
  alSeleccionar,
}: PropiedadesTarjetaModo) {
  const colorTexto = modo.colorAcento === "amarillo" ? "#3F2D03" : "#022C33";
  const colorTextoSecundario =
    modo.colorAcento === "amarillo" ? "#6B4E0A" : "#0A4A52";

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
        group relative flex h-full w-full flex-1 flex-col
        items-center justify-center px-6 py-16
        text-center opacity-0
        transition-all duration-700 ease-claridata-expo
        ${estaEnHover ? "scale-[1.02] brightness-[1.15]" : "scale-100 brightness-100"}
      `}
    >
      {/*
        PUNTO DE PREPARACIÓN — FASE SIGUIENTE:
        Aquí se agregará la lógica de expansión a pantalla completa al hacer click.
        El estado `modoSeleccionado` ya existe en SelectorModo y ya controla el
        delay de 550ms antes de la navegación. La fase futura debe:
        1. Recibir una prop `estaExpandiendo` (booleano) en este componente.
        2. Agregar clases condicionales de ancho/posición cuando estaExpandiendo === true.
        3. Agregar una clase de "fade-out" para la mitad NO seleccionada.
        No se implementa todavía — solo se deja documentado el punto exacto.
      */}

      <h2
        style={{ color: colorTexto }}
        className={`
          text-4xl font-bold tracking-tight transition-transform duration-500
          md:text-5xl
          ${estaEnHover ? "scale-[1.03]" : "scale-100"}
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