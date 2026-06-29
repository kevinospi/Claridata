import { DatasetRespuesta, InformeRespuesta } from "@/tipos/api";

interface PropiedadesVistaResultadoAnalisis {
  dataset: DatasetRespuesta;
  informe: InformeRespuesta;
  alAnalizarOtro: () => void;
}

function formatearFecha(fechaIso: string): string {
  return new Date(fechaIso).toLocaleString("es-CO", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function calcularPorcentajeNulos(informe: InformeRespuesta): number {
  const valoresNulos = informe.estadisticas_descriptivas?.valores_nulos;
  const metadatos = informe.estadisticas_descriptivas?.metadatos;

  if (!valoresNulos || !metadatos) return 0;

  const totalCeldas = metadatos.numero_filas * metadatos.numero_columnas;
  if (totalCeldas === 0) return 0;

  return (valoresNulos.total / totalCeldas) * 100;
}

interface DatoResumenProps {
  etiqueta: string;
  valor: string;
}

function DatoResumen({ etiqueta, valor }: DatoResumenProps) {
  return (
    <div className="flex flex-col gap-1 rounded-2xl border border-white/10 bg-white/[0.03] px-6 py-5">
      <p className="text-sm text-claridata-textoSecundario">{etiqueta}</p>
      <p className="text-2xl font-semibold text-claridata-texto">{valor}</p>
    </div>
  );
}

export function VistaResultadoAnalisis({
  dataset,
  informe,
  alAnalizarOtro,
}: PropiedadesVistaResultadoAnalisis) {
  const clasificacion = informe.estadisticas_descriptivas?.clasificacion_variables;
  const porcentajeNulos = calcularPorcentajeNulos(informe);

  return (
    <div className="flex w-full flex-col gap-8">
      <div className="text-center">
        <p className="text-sm font-medium uppercase tracking-wide text-claridata-marca">
          Análisis completado
        </p>
        <h2 className="mt-2 text-2xl font-bold text-claridata-texto">
          {dataset.nombre_archivo}
        </h2>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-3">
        <DatoResumen
          etiqueta="Filas"
          valor={dataset.numero_filas?.toLocaleString("es-CO") ?? "—"}
        />
        <DatoResumen
          etiqueta="Columnas"
          valor={dataset.numero_columnas?.toLocaleString("es-CO") ?? "—"}
        />
        <DatoResumen
          etiqueta="Variables numéricas"
          valor={clasificacion?.numericas.length.toString() ?? "—"}
        />
        <DatoResumen
          etiqueta="Variables categóricas"
          valor={clasificacion?.categoricas.length.toString() ?? "—"}
        />
        <DatoResumen
          etiqueta="Valores nulos"
          valor={`${porcentajeNulos.toFixed(1)}%`}
        />
        <DatoResumen
          etiqueta="Estado del análisis"
          valor={informe.guardado ? "Guardado" : "Analizado"}
        />
      </div>

      <p className="text-center text-sm text-claridata-textoSecundario">
        Análisis realizado el {formatearFecha(informe.fecha_creacion)}
      </p>

      <button
        type="button"
        onClick={alAnalizarOtro}
        className="mx-auto rounded-full border border-white/15 px-6 py-3 text-sm font-medium text-claridata-textoSecundario transition-colors duration-300 hover:border-white/30 hover:text-claridata-texto"
      >
        Analizar otro archivo
      </button>
    </div>
  );
}