import { SeccionInterpretacionRespuesta } from "@/tipos/api";

const ICONO_SECCION: Record<string, string> = {
  RESUMEN_GENERAL: "📋",
  VARIABLES_DESTACADAS: "📊",
  PATRONES_DETECTADOS: "🔍",
  CALIDAD_DATOS: "🛡️",
  RELACIONES_ENCONTRADAS: "🔗",
  IMPLICACIONES: "⚠️",
  RECOMENDACIONES_ANALITICAS: "💡",
};

interface PropiedadesSeccionInterpretacion {
  secciones: SeccionInterpretacionRespuesta[];
}

function TarjetaSeccion({
  seccion,
}: {
  seccion: SeccionInterpretacionRespuesta;
}) {
  const icono = ICONO_SECCION[seccion.tipo] ?? "📄";

  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-white/10 bg-white/[0.02] px-6 py-5">
      <div className="flex items-center gap-2">
        <span className="text-base">{icono}</span>
        <h4 className="text-sm font-semibold text-claridata-texto">
          {seccion.titulo}
        </h4>
      </div>

      <div className="flex flex-col gap-2">
        {seccion.parrafos.map((parrafo, indice) => (
          <p
            key={indice}
            className="text-sm leading-relaxed text-claridata-textoSecundario"
          >
            {parrafo}
          </p>
        ))}
      </div>
    </div>
  );
}

export function SeccionInterpretacion({
  secciones,
}: PropiedadesSeccionInterpretacion) {
  if (secciones.length === 0) return null;

  return (
    <div className="flex flex-col gap-4">
      <h3 className="text-base font-semibold text-claridata-texto">
        Interpretación profesional
      </h3>
      <div className="flex flex-col gap-3">
        {secciones.map((seccion) => (
          <TarjetaSeccion key={seccion.tipo} seccion={seccion} />
        ))}
      </div>
    </div>
  );
}