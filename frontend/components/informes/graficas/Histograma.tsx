"use client";

import ReactECharts from "echarts-for-react";
import { VisualizacionRespuesta } from "@/tipos/api";

interface PropiedadesHistograma {
  visualizacion: VisualizacionRespuesta;
}

function generarBinsNormales(
  media: number,
  std: number,
  min: number,
  max: number,
  nBins = 12,
): { nombre: string; valor: number }[] {
  if (std === 0) return [{ nombre: `${media.toFixed(2)}`, valor: 1 }];

  const paso = (max - min) / nBins;
  const bins: { nombre: string; valor: number }[] = [];

  for (let i = 0; i < nBins; i++) {
    const x = min + paso * (i + 0.5);
    const z = (x - media) / std;
    const densidad = Math.exp(-0.5 * z * z) / (std * Math.sqrt(2 * Math.PI));
    bins.push({
      nombre: `${(min + paso * i).toFixed(1)}–${(min + paso * (i + 1)).toFixed(1)}`,
      valor: Math.round(densidad * paso * 100) / 100,
    });
  }
  return bins;
}

export function Histograma({ visualizacion }: PropiedadesHistograma) {
  const cfg = visualizacion.configuracion as any;
  const bins = generarBinsNormales(
    cfg.media ?? 0,
    cfg.desviacion_estandar ?? 1,
    cfg.minimo ?? 0,
    cfg.maximo ?? 10,
  );

  const opciones = {
    backgroundColor: "transparent",
    tooltip: {
      trigger: "axis",
      backgroundColor: "#1A2333",
      borderColor: "rgba(34,211,238,0.2)",
      textStyle: { color: "#E5E7EB" },
    },
    grid: { left: 40, right: 20, top: 20, bottom: 60 },
    xAxis: {
      type: "category",
      data: bins.map((b) => b.nombre),
      axisLabel: {
        color: "#94A3B8",
        fontSize: 10,
        rotate: 30,
      },
      axisLine: { lineStyle: { color: "rgba(255,255,255,0.1)" } },
    },
    yAxis: {
      type: "value",
      axisLabel: { color: "#94A3B8", fontSize: 10 },
      splitLine: { lineStyle: { color: "rgba(255,255,255,0.06)" } },
    },
    series: [
      {
        type: "bar",
        data: bins.map((b) => b.valor),
        itemStyle: {
          color: {
            type: "linear",
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: "#22D3EE" },
              { offset: 1, color: "rgba(34,211,238,0.2)" },
            ],
          },
          borderRadius: [3, 3, 0, 0],
        },
        markLine: {
          symbol: "none",
          data: [
            {
              xAxis: Math.floor(bins.length / 2),
              lineStyle: { color: "#F59E0B", type: "dashed", width: 2 },
              label: { formatter: `Media: ${(cfg.media ?? 0).toFixed(2)}`, color: "#F59E0B" },
            },
          ],
        },
      },
    ],
  };

  return <ReactECharts option={opciones} style={{ height: 260 }} />;
}