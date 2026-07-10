"use client";

import { useEffect, useRef, useState } from "react";
import { redondear } from "@/lib/laboratorios/calculos";

interface PropiedadesTarjetaIndicador {
  etiqueta: string;
  simbolo: string;
  valor: number;
  color: string;
  moda?: number[];
}

function TarjetaIndicador({
  etiqueta,
  simbolo,
  valor,
  color,
  moda,
}: PropiedadesTarjetaIndicador) {
  const valorAnteriorRef = useRef<number>(valor);
  const [animando, setAnimando] = useState(false);

  useEffect(() => {
    if (Math.abs(valor - valorAnteriorRef.current) > 0.001) {
      setAnimando(true);
      const id = setTimeout(() => setAnimando(false), 400);
      valorAnteriorRef.current = valor;
      return () => clearTimeout(id);
    }
  }, [valor]);

  const esMultipleModa = moda && moda.length > 1;
  const sinModa = moda && moda.length === 0;

  return (
    <div
      className="flex flex-col gap-2 rounded-2xl border bg-white/[0.03] px-5 py-5"
      style={{ borderColor: `${color}30` }}
    >
      <div className="flex items-center gap-2">
        <span
          className="text-xl font-bold"
          style={{ color }}
        >
          {simbolo}
        </span>
        <span className="text-sm font-medium text-claridata-textoSecundario">
          {etiqueta}
        </span>
      </div>

      {sinModa ? (
        <p className="text-sm text-claridata-textoSecundario italic">
          Sin moda
        </p>
      ) : esMultipleModa ? (
        <div className="flex flex-wrap gap-1">
          {moda.map((m) => (
            <span
              key={m}
              className="rounded-lg px-2 py-0.5 text-lg font-bold"
              style={{ color, backgroundColor: `${color}15` }}
            >
              {redondear(m, 1)}
            </span>
          ))}
        </div>
      ) : (
        <span
          className="text-2xl font-bold transition-all duration-300"
          style={{
            color,
            transform: animando ? "scale(1.08)" : "scale(1)",
            display: "inline-block",
          }}
        >
          {redondear(valor, 2)}
        </span>
      )}
    </div>
  );
}

interface PropiedadesPanelIndicadores {
  media: number;
  mediana: number;
  moda: number[];
}

export function PanelIndicadores({
  media,
  mediana,
  moda,
}: PropiedadesPanelIndicadores) {
  return (
    <div className="grid grid-cols-3 gap-3">
      <TarjetaIndicador
        etiqueta="Media"
        simbolo="x̄"
        valor={media}
        color="#F59E0B"
      />
      <TarjetaIndicador
        etiqueta="Mediana"
        simbolo="Me"
        valor={mediana}
        color="#10B981"
      />
      <TarjetaIndicador
        etiqueta="Moda"
        simbolo="Mo"
        valor={moda[0] ?? 0}
        color="#A78BFA"
        moda={moda}
      />
    </div>
  );
}