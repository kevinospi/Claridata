"use client";

import ReactECharts from "echarts-for-react";
import { VisualizacionRespuesta } from "@/tipos/api";

interface PropiedadesScatterPlot {
  visualizacion: VisualizacionRespuesta;
}

export function ScatterPlot({ visualizacion }: PropiedadesScatterPlot) {
  const cfg = visualizacion.configuracion as any;
  const coef = cfg.coeficiente ?? 0;
  const colX = cfg.columna_x ?? visualizacion.variables[0] ?? "X";
  const colY = cfg.columna_y ?? visualizacion.variables[1] ?? "Y";

  const colorLinea = coef >= 0 ? "#22D3EE" : "#F87171";

  const opciones = {
    backgroundColor: "transparent",
    tooltip: {
      trigger: "item",
      backgroundColor: "#1A2333",
      borderColor: "rgba(34,211,238,0.2)",
      textStyle: { color: "#E5E7EB" },
      formatter: `r = ${coef.toFixed(3)}`,
    },
    grid: { left: 50, right: 20, top: 30, bottom: 50 },
    xAxis: {
      name: colX,
      nameLocation: "middle",
      nameGap: 30,
      nameTextStyle: { color: "#94A3B8" },
      axisLabel: { color: "#94A3B8", fontSize: 10 },
      splitLine: { lineStyle: { color: "rgba(255,255,255,0.06)" } },
    },
    yAxis: {
      name: colY,
      nameLocation: "middle",
      nameGap: 40,
      nameTextStyle: { color: "#94A3B8" },
      axisLabel: { color: "#94A3B8", fontSize: 10 },
      splitLine: { lineStyle: { color: "rgba(255,255,255,0.06)" } },
    },
    series: [
      {
        type: "scatter",
        symbolSize: 8,
        data: Array.from({ length: 30 }, (_, i) => {
          const x = i / 29;
          const y = coef * x + (Math.random() - 0.5) * 0.3;
          return [x, Math.max(0, Math.min(1, y))];
        }),
        itemStyle: {
          color: colorLinea,
          opacity: 0.7,
        },
      },
    ],
    graphic: [
      {
        type: "text",
        left: "center",
        top: 5,
        style: {
          text: `r = ${coef.toFixed(3)}`,
          fill: colorLinea,
          font: "bold 13px sans-serif",
        },
      },
    ],
  };

  return (
    <div className="flex flex-col gap-1">
      <ReactECharts option={opciones} style={{ height: 260 }} />
      <p className="text-center text-xs text-claridata-textoSecundario">
        Representación aproximada de la tendencia. Los valores individuales no están disponibles en este informe.
      </p>
    </div>
  );
}