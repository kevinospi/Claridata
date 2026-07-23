import { PrioridadRecomendacion, RecomendacionRespuesta } from "@/tipos/api";

const CONFIG_PRIORIDAD: Record <
  PrioridadRecomendacion,
  { etiqueta: string; colorTexto: string; colorFondo: string; colorBorde: string }
> = {
  ALTA: {
    etiqueta: "Alta",
    colorTexto: "#FCA5A5",
    colorFondo: "rgba(239, 68, 68, 0.08)",
    colorBorde: "rgba(239, 68, 68, 0.25)",
  },
  MEDIA: {
    etiqueta: "Media",
    colorTexto: "#FDE047",
    colorFondo: "rgba(234, 179, 8, 0.08)",
    colorBorde: "rgba(234, 179, 8, 0.25)",
  },
  BAJA: {
    etiqueta: "Baja",
    colorTexto: "#86EFAC",
    colorFondo: "rgba(34, 197, 94, 0.08)",
    colorBorde: "rgba(34, 197, 94, 0.25)",
  },
};

const ORDEN_PRIORIDAD: PrioridadRecomendacion[] = ["ALTA", "MEDIA", "BAJA"];

function TarjetaRecomendacion({
  recomendacion,
}: {
  recomendacion: RecomendacionRespuesta;
}) {
  const config = CONFIG_PRIORIDAD[recomendacion.prioridad];

  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-white/10 bg-white/[0.02] px-5 py-5">
      <div className="flex items-start justify-between gap-3">
        <p className="text-sm font-semibold text-claridata-texto leading-snug">
          {recomendacion.titulo}
        </p>
        <span
          className="shrink-0 rounded-full px-2.5 py-0.5 text-xs font-medium"
          style={{
            color: config.colorTexto,
            backgroundColor: config.colorFondo,
            border: `1px solid ${config.colorBorde}`,
          }}
        >
          {config.etiqueta}
        </span>
      </div>

      <p className="text-xs font-medium uppercase tracking-wide"
        style={{ color: config.colorTexto, opacity: 0.7 }}>
        {recomendacion.categoria}
      </p>

      <p className="text-sm text-claridata-textoSecundario leading-relaxed">
        {recomendacion.razon}
      </p>

      <div
        className="rounded-xl px-4 py-3"
        style={{ backgroundColor: "rgba(255,255,255,0.03)" }}
      >
        <p className="text-xs font-semibold text-claridata-textoSecundario mb-1">
          ¿Qué hacer?
        </p>
        <p className="text-sm text-claridata-textoSecundario leading-relaxed whitespace-pre-line">
          {recomendacion.accion}
        </p>
      </div>
    </div>
  );
}

interface PropiedadesSeccionRecomendaciones {
  recomendaciones: RecomendacionRespuesta[];
}

export function SeccionRecomendaciones({
  recomendaciones,
}: PropiedadesSeccionRecomendaciones) {
  if (recomendaciones.length === 0) return null;

  const agrupadas = ORDEN_PRIORIDAD.reduce <
    Record<PrioridadRecomendacion, RecomendacionRespuesta[]>
  >(
    (acc, p) => ({ ...acc, [p]: [] }),
    { ALTA: [], MEDIA: [], BAJA: [] },
  );

  for (const r of recomendaciones) {
    agrupadas[r.prioridad].push(r);
  }

  const conteo = ORDEN_PRIORIDAD.filter(
    (p) => agrupadas[p].length > 0,
  );

  return (
    <div className="flex flex-col gap-5">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-semibold text-claridata-texto">
          Recomendaciones
        </h3>
        <div className="flex items-center gap-2">
          {conteo.map((p) => (
            <span
              key={p}
              className="text-xs rounded-full px-2 py-0.5"
              style={{
                color: CONFIG_PRIORIDAD[p].colorTexto,
                backgroundColor: CONFIG_PRIORIDAD[p].colorFondo,
              }}
            >
              {CONFIG_PRIORIDAD[p].etiqueta}: {agrupadas[p].length}
            </span>
          ))}
        </div>
      </div>

      {ORDEN_PRIORIDAD.filter((p) => agrupadas[p].length > 0).map((prioridad) => (
        <div key={prioridad} className="flex flex-col gap-3">
          <p
            className="text-xs font-semibold uppercase tracking-widest"
            style={{ color: CONFIG_PRIORIDAD[prioridad].colorTexto, opacity: 0.8 }}
          >
            Prioridad {CONFIG_PRIORIDAD[prioridad].etiqueta}
          </p>
          {agrupadas[prioridad].map((r, i) => (
            <TarjetaRecomendacion key={`${r.titulo}-${i}`} recomendacion={r} />
          ))}
        </div>
      ))}
    </div>
  );
}