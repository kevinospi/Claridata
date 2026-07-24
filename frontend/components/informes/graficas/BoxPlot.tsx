"use client";

import ReactECharts from "echarts-for-react";
import { VisualizacionRespuesta } from "@/tipos/api";

interface PropiedadesBoxPlot {
  visualizacion: VisualizacionRespuesta;
}

export function BoxPlot({ visualizacion }: PropiedadesBoxPlot) {
  const cfg = visualizacion.configuracion as any;
  const columna = visualizacion.variables[0] ?? "";

  const q1 = cfg.q1 ?? 0;
  const q3 = cfg.q3 ?? 1;
  const iqr = cfg.iqr ?? q3 - q1;
  const limInf = cfg.limite_inferior ?? q1 - 1.5 * iqr;
  const limSup = cfg.limite_superior ?? q3 + 1.5 * iqr;
  const mediana = (q1 + q3) / 2;

  const opciones = {
    backgroundColor: "transparent",
    tooltip: {
      trigger: "item",
      backgroundColor: "#1A2333",
      borderColor: "rgba(34,211,238,0.2)",
      textStyle: { color: "#E5E7EB" },
      formatter: (params: any) => {
        if (params.seriesType === "boxplot") {
          const d = params.data;
          return `
            <b>${columna}</b><br/>
            Mín: ${d[1]?.toFixed(2)}<br/>
            Q1: ${d[2]?.toFixed(2)}<br/>
            Mediana: ${d[3]?.toFixed(2)}<br/>
            Q3: ${d[4]?.toFixed(2)}<br/>
            Máx: ${d[5]?.toFixed(2)}
          `;
        }
        return `Outlier: ${params.data[1]?.toFixed(2)}`;
      },
    },
    grid: { left: 60, right: 20, top: 20, bottom: 30 },
    xAxis: {
      type: "category",
      data: [columna],
      axisLabel: { color: "#94A3B8" },
      axisLine: { lineStyle: { color: "rgba(255,255,255,0.1)" } },
    },
    yAxis: {
      type: "value",
      axisLabel: { color: "#94A3B8", fontSize: 10 },
      splitLine: { lineStyle: { color: "rgba(255,255,255,0.06)" } },
    },
    series: [
      {
        type: "boxplot",
        data: [[limInf, q1, mediana, q3, limSup]],
        itemStyle: {
          color: "rgba(34,211,238,0.15)",
          borderColor: "#22D3EE",
          borderWidth: 2,
        },
      },
    ],
  };

  return (
    <div className="flex flex-col gap-2">
      <ReactECharts option={opciones} style={{ height: 260 }} />
      {cfg.cantidad_outliers > 0 && (
        <p className="text-center text-xs text-amber-400">
          ⚠️ {cfg.cantidad_outliers} valor(es) atípico(s) fuera de [{limInf.toFixed(2)}, {limSup.toFixed(2)}]
        </p>
      )}
    </div>
  );
}