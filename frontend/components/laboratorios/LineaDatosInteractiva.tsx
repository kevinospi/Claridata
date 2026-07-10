"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { PuntoDato as TipoPunto } from "@/tipos/laboratorio";
import { PuntoDato } from "./PuntoDato";
import { clampear } from "@/lib/laboratorios/calculos";

interface PropiedadesLineaDatosInteractiva {
  puntos: TipoPunto[];
  valorMinimo: number;
  valorMaximo: number;
  etiquetaUnidad: string;
  media: number;
  mediana: number;
  alMoverPunto: (id: string, nuevoValor: number) => void;
  alEliminarPunto: (id: string) => void;
}

const ALTURA_SVG = 160;
const RADIO_PUNTO = 12;
const PADDING_HORIZONTAL = 48;
const COLOR_PUNTO = "#22D3EE";
const COLOR_PUNTO_HOVER = "#67E8F9";
const COLOR_MEDIA = "#F59E0B";
const COLOR_MEDIANA = "#10B981";

export function LineaDatosInteractiva({
  puntos,
  valorMinimo,
  valorMaximo,
  etiquetaUnidad,
  media,
  mediana,
  alMoverPunto,
  alEliminarPunto,
}: PropiedadesLineaDatosInteractiva) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [anchoPx, setAnchoPx] = useState(700);
  const [arrastrando, setArrastrando] = useState<string | null>(null);

  useEffect(() => {
    const observer = new ResizeObserver((entradas) => {
      for (const entrada of entradas) {
        setAnchoPx(entrada.contentRect.width);
      }
    });

    if (svgRef.current) {
      observer.observe(svgRef.current.parentElement!);
    }

    return () => observer.disconnect();
  }, []);

  const valorAPx = useCallback(
    (valor: number): number => {
      const rango = valorMaximo - valorMinimo;
      const fraccion = (valor - valorMinimo) / rango;
      return PADDING_HORIZONTAL + fraccion * (anchoPx - PADDING_HORIZONTAL * 2);
    },
    [anchoPx, valorMinimo, valorMaximo],
  );

  const pxAValor = useCallback(
    (px: number): number => {
      const rango = valorMaximo - valorMinimo;
      const fraccion =
        (px - PADDING_HORIZONTAL) / (anchoPx - PADDING_HORIZONTAL * 2);
      return clampear(
        valorMinimo + fraccion * rango,
        valorMinimo,
        valorMaximo,
      );
    },
    [anchoPx, valorMinimo, valorMaximo],
  );

  const obtenerXDelEvento = useCallback(
    (e: MouseEvent | TouchEvent): number => {
      const rect = svgRef.current?.getBoundingClientRect();
      if (!rect) return 0;

      if ("touches" in e) {
        return e.touches[0].clientX - rect.left;
      }
      return e.clientX - rect.left;
    },
    [],
  );

  const iniciarArrastre = useCallback(
    (id: string, _eventoInicial: React.MouseEvent | React.TouchEvent) => {
      setArrastrando(id);

      const manejarMovimiento = (e: MouseEvent | TouchEvent) => {
        e.preventDefault();
        const x = obtenerXDelEvento(e);
        const nuevoValor = pxAValor(x);
        alMoverPunto(id, Math.round(nuevoValor * 10) / 10);
      };

      const terminarArrastre = () => {
        setArrastrando(null);
        window.removeEventListener("mousemove", manejarMovimiento);
        window.removeEventListener("mouseup", terminarArrastre);
        window.removeEventListener("touchmove", manejarMovimiento);
        window.removeEventListener("touchend", terminarArrastre);
      };

      window.addEventListener("mousemove", manejarMovimiento);
      window.addEventListener("mouseup", terminarArrastre);
      window.addEventListener("touchmove", manejarMovimiento, {
        passive: false,
      });
      window.addEventListener("touchend", terminarArrastre);
    },
    [pxAValor, alMoverPunto, obtenerXDelEvento],
  );

  const cy = ALTURA_SVG / 2;
  const xMedia = valorAPx(media);
  const xMediana = valorAPx(mediana);

  return (
    <div className="w-full select-none">
      <svg
        ref={svgRef}
        width="100%"
        height={ALTURA_SVG}
        className="overflow-visible"
      >
        <line
          x1={PADDING_HORIZONTAL}
          y1={cy}
          x2={anchoPx - PADDING_HORIZONTAL}
          y2={cy}
          stroke="#1E293B"
          strokeWidth={3}
          strokeLinecap="round"
        />

        <line
          x1={valorAPx(valorMinimo)}
          y1={cy - 6}
          x2={valorAPx(valorMinimo)}
          y2={cy + 6}
          stroke="#334155"
          strokeWidth={2}
        />
        <text
          x={valorAPx(valorMinimo)}
          y={cy + 22}
          textAnchor="middle"
          fill="#475569"
          fontSize="11"
        >
          {etiquetaUnidad}{valorMinimo}
        </text>

        <line
          x1={valorAPx(valorMaximo)}
          y1={cy - 6}
          x2={valorAPx(valorMaximo)}
          y2={cy + 6}
          stroke="#334155"
          strokeWidth={2}
        />
        <text
          x={valorAPx(valorMaximo)}
          y={cy + 22}
          textAnchor="middle"
          fill="#475569"
          fontSize="11"
        >
          {etiquetaUnidad}{valorMaximo}
        </text>

        <line
          x1={xMedia}
          y1={16}
          x2={xMedia}
          y2={ALTURA_SVG - 16}
          stroke={COLOR_MEDIA}
          strokeWidth={2}
          strokeDasharray="4 3"
          opacity={0.7}
          style={{ transition: "x1 80ms ease-out, x2 80ms ease-out" }}
        />
        <text
          x={xMedia}
          y={12}
          textAnchor="middle"
          fill={COLOR_MEDIA}
          fontSize="10"
          fontWeight="600"
        >
          x̄
        </text>

        <line
          x1={xMediana}
          y1={16}
          x2={xMediana}
          y2={ALTURA_SVG - 16}
          stroke={COLOR_MEDIANA}
          strokeWidth={2}
          strokeDasharray="4 3"
          opacity={0.7}
          style={{ transition: "x1 80ms ease-out, x2 80ms ease-out" }}
        />
        <text
          x={xMediana}
          y={ALTURA_SVG - 4}
          textAnchor="middle"
          fill={COLOR_MEDIANA}
          fontSize="10"
          fontWeight="600"
        >
          Me
        </text>

        {puntos.map((punto) => (
          <PuntoDato
            key={punto.id}
            id={punto.id}
            cx={valorAPx(punto.valor)}
            cy={cy}
            radio={arrastrando === punto.id ? RADIO_PUNTO * 1.15 : RADIO_PUNTO}
            color={arrastrando === punto.id ? COLOR_PUNTO_HOVER : COLOR_PUNTO}
            colorHover={COLOR_PUNTO_HOVER}
            valor={punto.valor}
            etiquetaUnidad={etiquetaUnidad}
            alIniciarArrastre={iniciarArrastre}
            alEliminar={alEliminarPunto}
          />
        ))}
      </svg>
    </div>
  );
}