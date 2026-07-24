"use client";

import ReactECharts from "echarts-for-react";
import { VisualizacionRespuesta } from "@/tipos/api";

interface PropiedadesHeatmap {
  visualizacion: VisualizacionRespuesta;
}

export function Heatmap({ visualizacion }: PropiedadesHeatmap) {
  const cfg = visualizacion.configuracion as any;
  const variables: string[] = cfg.variables ?? [];
  const matriz: Record<string, Record<string, number>> = cfg.matriz ?? {};

  const datos: [number, number, number][] = [];
  variables.forEach((varY, i) => {
    variables.forEach((varX, j) => {
      const valor = matriz?.[varX]?.[varY] ?? matriz?.[varY]?.[varX] ?? (i === j ? 1 : 0);
      datos.push([j, i, parseFloat(valor.toFixed(3))]);
    });
  });

  const opciones = {
    backgroundColor: "transparent",
    tooltip: {
      position: "top",
      backgroundColor: "#1A2333",
      borderColor: "rgba(34,211,238,0.2)",
      textStyle: { color: "#E5E7EB" },
      formatter: (params: any) =>
        `${variables[params.data[1]]} ↔ ${variables[params.data[0]]}: <b>${params.data[2]}</b>`,
    },
    grid: { left: 100, right: 20, top: 20, bottom: 100 },
    xAxis: {
      type: "category",
      data: variables,
      axisLabel: { color: "#94A3B8", fontSize: 10, rotate: 30 },
      axisLine: { lineStyle: { color: "rgba(255,255,255,0.1)" } },
      splitArea: { show: true, areaStyle: { color: ["rgba(255,255,255,0.01)", "transparent"] } },
    },
    yAxis: {
      type: "category",
      data: variables,
      axisLabel: { color: "#94A3B8", fontSize: 10 },
      axisLine: { lineStyle: { color: "rgba(255,255,255,0.1)" } },
      splitArea: { show: true, areaStyle: { color: ["rgba(255,255,255,0.01)", "transparent"] } },
    },
    visualMap: {
      min: -1,
      max: 1,
      calculable: true,
      orient: "horizontal",
      left: "center",
      bottom: 5,
      inRange: {
        color: ["#F87171", "#1A2333", "#22D3EE"],
      },
      textStyle: { color: "#94A3B8" },
    },
    series: [
      {
        type: "heatmap",
        data: datos,
        label: {
          show: variables.length <= 8,
          color: "#E5E7EB",
          fontSize: 10,
          formatter: (params: any) => params.data[2].toFixed(2),
        },
        emphasis: {
          itemStyle: { shadowBlur: 10, shadowColor: "rgba(34,211,238,0.5)" },
        },
      },
    ],
  };

  return <ReactECharts option={opciones} style={{ height: Math.max(280, variables.length * 40 + 120) }} />;
}