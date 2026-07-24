"use client";

export function GraficasPlaceholder() {
  return (
    <div className="flex flex-col items-center gap-4 rounded-2xl border border-dashed border-white/15 py-16 text-center">
      <span className="text-5xl">📈</span>
      <p className="text-base font-semibold text-claridata-texto">
        Gráficas en desarrollo
      </p>
      <p className="max-w-sm text-sm text-claridata-textoSecundario">
        La siguiente fase conectará visualizaciones interactivas (histogramas,
        scatter plots, heatmaps de correlación) directamente con los datos de
        este informe.
      </p>
    </div>
  );
}