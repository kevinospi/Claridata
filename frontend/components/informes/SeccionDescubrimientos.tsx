import { DescubrimientoRespuesta, SeveridadDescubrimiento } from "@/tipos/api";

const CONFIG_SEVERIDAD: Record < 
  SeveridadDescubrimiento,
  { emoji: string; colorBorde: string; colorFondo: string; colorTexto: string }
> = {
  INFORMATIVO: {
    emoji: "🔵",
    colorBorde: "rgba(59, 130, 246, 0.3)",
    colorFondo: "rgba(59, 130, 246, 0.05)",
    colorTexto: "#93C5FD",
  },
  ATENCION: {
    emoji: "🟡",
    colorBorde: "rgba(234, 179, 8, 0.3)",
    colorFondo: "rgba(234, 179, 8, 0.05)",
    colorTexto: "#FDE047",
  },
  IMPORTANTE: {
    emoji: "🟠",
    colorBorde: "rgba(249, 115, 22, 0.3)",
    colorFondo: "rgba(249, 115, 22, 0.05)",
    colorTexto: "#FDBA74",
  },
  CRITICO: {
    emoji: "🔴",
    colorBorde: "rgba(239, 68, 68, 0.3)",
    colorFondo: "rgba(239, 68, 68, 0.05)",
    colorTexto: "#FCA5A5",
  },
};

const ORDEN_SEVERIDAD: SeveridadDescubrimiento[] = [
  "CRITICO",
  "IMPORTANTE",
  "ATENCION",
  "INFORMATIVO",
];

interface PropiedadesSeccionDescubrimientos {
  descubrimientos: DescubrimientoRespuesta[];
}

function TarjetaDescubrimiento({
  descubrimiento,
}: {
  descubrimiento: DescubrimientoRespuesta;
}) {
  const config = CONFIG_SEVERIDAD[descubrimiento.severidad];

  return (
    <div
      className="flex flex-col gap-2 rounded-xl border px-5 py-4"
      style={{
        borderColor: config.colorBorde,
        backgroundColor: config.colorFondo,
      }}
    >
      <div className="flex items-start gap-2">
        <span className="text-base leading-snug">{config.emoji}</span>
        <div className="flex flex-col gap-1">
          <p
            className="text-sm font-semibold leading-snug"
            style={{ color: config.colorTexto }}
          >
            {descubrimiento.titulo}
          </p>
          {descubrimiento.columna && (
            <p className="text-xs text-claridata-textoSecundario">
              Variable: <span className="font-mono">{descubrimiento.columna}</span>
            </p>
          )}
        </div>
      </div>

      <p className="text-sm text-claridata-textoSecundario leading-relaxed">
        {descubrimiento.descripcion}
      </p>

      {descubrimiento.recomendacion && (
        <p className="text-xs text-claridata-textoSecundario border-t border-white/5 pt-2 mt-1 leading-relaxed">
          💡 {descubrimiento.recomendacion}
        </p>
      )}
    </div>
  );
}

export function SeccionDescubrimientos({
  descubrimientos,
}: PropiedadesSeccionDescubrimientos) {
  if (descubrimientos.length === 0) {
    return (
      <div className="flex flex-col gap-3">
        <h3 className="text-base font-semibold text-claridata-texto">
          Descubrimientos automáticos
        </h3>
        <p className="text-sm text-claridata-textoSecundario">
          No se detectaron patrones especiales en este dataset.
        </p>
      </div>
    );
  }

  const descubrimientosOrdenados = [...descubrimientos].sort(
    (a, b) =>
      ORDEN_SEVERIDAD.indexOf(a.severidad) -
      ORDEN_SEVERIDAD.indexOf(b.severidad),
  );

  const conteo: Record<SeveridadDescubrimiento, number> = {
    CRITICO: 0,
    IMPORTANTE: 0,
    ATENCION: 0,
    INFORMATIVO: 0,
  };

  for (const d of descubrimientos) {
    conteo[d.severidad]++;
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-semibold text-claridata-texto">
          Descubrimientos automáticos
        </h3>
        <div className="flex items-center gap-2">
          {ORDEN_SEVERIDAD.filter((s) => conteo[s] > 0).map((s) => (
            <span
              key={s}
              className="text-xs rounded-full px-2 py-0.5"
              style={{
                color: CONFIG_SEVERIDAD[s].colorTexto,
                backgroundColor: CONFIG_SEVERIDAD[s].colorFondo,
              }}
            >
              {CONFIG_SEVERIDAD[s].emoji} {conteo[s]}
            </span>
          ))}
        </div>
      </div>

      <div className="flex flex-col gap-3">
        {descubrimientosOrdenados.map((descubrimiento, indice) => (
          <TarjetaDescubrimiento
            key={`${descubrimiento.tipo}-${descubrimiento.columna ?? "global"}-${indice}`}
            descubrimiento={descubrimiento}
          />
        ))}
      </div>
    </div>
  );
}