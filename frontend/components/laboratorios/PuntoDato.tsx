"use client";

import { useRef, useState } from "react";

interface PropiedadesPuntoDato {
  id: string;
  cx: number;
  cy: number;
  radio: number;
  color: string;
  colorHover: string;
  valor: number;
  etiquetaUnidad: string;
  alIniciarArrastre: (id: string, eventoInicial: React.MouseEvent | React.TouchEvent) => void;
  alEliminar: (id: string) => void;
}

export function PuntoDato({
  id,
  cx,
  cy,
  radio,
  color,
  colorHover,
  valor,
  etiquetaUnidad,
  alIniciarArrastre,
  alEliminar,
}: PropiedadesPuntoDato) {
  const [enHover, setEnHover] = useState(false);
  const [editando, setEditando] = useState(false);

  const radioActual = enHover ? radio * 1.25 : radio;

  return (
    <g
      onMouseEnter={() => setEnHover(true)}
      onMouseLeave={() => setEnHover(false)}
      style={{ cursor: "grab" }}
    >
      <circle
        cx={cx}
        cy={cy}
        r={radioActual}
        fill={enHover ? colorHover : color}
        style={{
          transition: "r 150ms ease-out, fill 150ms ease-out",
          filter: enHover
            ? "drop-shadow(0 0 8px rgba(34, 211, 238, 0.5))"
            : "none",
        }}
        onMouseDown={(e) => {
          e.preventDefault();
          alIniciarArrastre(id, e);
        }}
        onDoubleClick={(e) => {
          e.stopPropagation();
          setEditando(true);
        }}
      />

      <text
        x={cx}
        y={cy - radio - 10}
        textAnchor="middle"
        fill="#94A3B8"
        fontSize="11"
        style={{ pointerEvents: "none", userSelect: "none" }}
      >
        {etiquetaUnidad}{valor.toFixed(1)}
      </text>

      {enHover && !editando && (
        <g
          onClick={(e) => {
            e.stopPropagation();
            alEliminar(id);
          }}
          style={{ cursor: "pointer" }}
        >
          <circle cx={cx + radio} cy={cy - radio} r={7} fill="#EF4444" opacity={0.9} />
          <text
            x={cx + radio}
            y={cy - radio + 4}
            textAnchor="middle"
            fill="white"
            fontSize="10"
            style={{ pointerEvents: "none", userSelect: "none" }}
          >
            ×
          </text>
        </g>
      )}
    </g>
  );
}