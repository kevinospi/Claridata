"use client";

import { useReducer, useMemo } from "react";
import { ConfiguracionLaboratorio } from "@/tipos/laboratorio";
import { calcularTodos } from "@/lib/laboratorios/calculos";
import {
  ESTADO_INICIAL_SALARIOS,
  reducerLaboratorio,
} from "@/lib/laboratorios/estadoLaboratorio";
import { detectarMomento } from "@/lib/laboratorios/narrativa";
import { LineaDatosInteractiva } from "./LineaDatosInteractiva";
import { PanelIndicadores } from "./PanelIndicadores";
import { ControlesLaboratorio } from "./ControlesLaboratorio";
import { PreguntaDinamica } from "./PreguntaDinamica";
import { RetosLaboratorio } from "./RetosLaboratorio";
import { useState } from "react";

const CONFIGURACION: ConfiguracionLaboratorio = {
  valorMinimo: 0,
  valorMaximo: 20,
  etiquetaUnidad: "$",
  titulo: "Medidas de Tendencia Central",
  descripcionContexto:
    "Ocho jugadores del mismo equipo. Estos son sus salarios (en millones). Arrastra cualquier valor.",
};

export function LaboratorioMedia() {
  const [estado, despachar] = useReducer(
    reducerLaboratorio,
    ESTADO_INICIAL_SALARIOS,
  );
  const [retoActivo, setRetoActivo] = useState<string | null>(null);

  const resultados = useMemo(
    () => calcularTodos(estado.puntos),
    [estado.puntos],
  );

  const momento = useMemo(
    () => detectarMomento(estado.puntos, resultados),
    [estado.puntos, resultados],
  );

  return (
    <div className="flex flex-col gap-8">
      <div className="text-center">
        <h1 className="text-3xl font-extrabold tracking-tight text-claridata-texto md:text-4xl">
          {CONFIGURACION.titulo}
        </h1>
        <p className="mx-auto mt-3 max-w-xl text-base text-claridata-textoSecundario">
          {CONFIGURACION.descripcionContexto}
        </p>
      </div>

      <div className="rounded-2xl border border-white/10 bg-white/[0.02] px-4 py-6">
        <LineaDatosInteractiva
          puntos={estado.puntos}
          valorMinimo={CONFIGURACION.valorMinimo}
          valorMaximo={CONFIGURACION.valorMaximo}
          etiquetaUnidad={CONFIGURACION.etiquetaUnidad}
          media={resultados.media}
          mediana={resultados.mediana}
          alMoverPunto={(id, nuevoValor) =>
            despachar({ tipo: "MOVER_PUNTO", id, nuevoValor })
          }
          alEliminarPunto={(id) =>
            despachar({ tipo: "ELIMINAR_PUNTO", id })
          }
        />
      </div>

      <PanelIndicadores
        media={resultados.media}
        mediana={resultados.mediana}
        moda={resultados.moda}
      />

      <PreguntaDinamica momento={momento} />

      <ControlesLaboratorio
        cantidadPuntos={estado.puntos.length}
        alAgregarPunto={() => despachar({ tipo: "AGREGAR_PUNTO" })}
      />

      <RetosLaboratorio
        retoActivo={retoActivo}
        alSeleccionarReto={setRetoActivo}
      />
    </div>
  );
}