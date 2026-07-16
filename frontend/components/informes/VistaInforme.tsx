"use client";

import { useState } from "react";
import { InformeDetalleRespuesta } from "@/tipos/api";
import { ModalRenombrarInforme } from "./ModalRenombrarInforme";
import { SeccionDescubrimientos } from "./SeccionDescubrimientos";
import { renombrarInforme } from "@/lib/api/informes";

interface PropiedadesVistaInforme {
  informe: InformeDetalleRespuesta;
  alActualizarInforme?: (informe: InformeDetalleRespuesta) => void;
  alAnalizarOtro?: () => void;
}

function formatearFecha(fechaIso: string): string {
  return new Date(fechaIso).toLocaleString("es-CO", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function calcularPorcentajeNulos(informe: InformeDetalleRespuesta): number {
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

export function VistaInforme({
  informe,
  alActualizarInforme,
  alAnalizarOtro,
}: PropiedadesVistaInforme) {
  const [modalAbierto, setModalAbierto] = useState(false);
  const [renombrando, setRenombrando] = useState(false);
  const [errorRenombrar, setErrorRenombrar] = useState<string | null>(null);

  const metadatos = informe.estadisticas_descriptivas?.metadatos;
  const clasificacion =
    informe.estadisticas_descriptivas?.clasificacion_variables;
  const porcentajeNulos = calcularPorcentajeNulos(informe);

  const manejarConfirmarRenombrar = async (nuevoTitulo: string) => {
    setRenombrando(true);
    setErrorRenombrar(null);

    try {
      const informeActualizado = await renombrarInforme(informe.id, nuevoTitulo);
      alActualizarInforme?.(informeActualizado);
      setModalAbierto(false);
    } catch {
      setErrorRenombrar(
        "No fue posible renombrar el informe. Intenta de nuevo.",
      );
    } finally {
      setRenombrando(false);
    }
  };

  return (
    <div className="flex w-full flex-col gap-8">
      <div className="text-center">
        <p className="text-sm font-medium uppercase tracking-wide text-claridata-marca">
          {informe.guardado ? "Informe guardado" : "Análisis completado"}
        </p>

        <div className="mt-2 flex items-center justify-center gap-3">
          <h2 className="text-2xl font-bold text-claridata-texto">
            {informe.titulo}
          </h2>

          {alActualizarInforme && (
            <button
              type="button"
              onClick={() => setModalAbierto(true)}
              aria-label="Renombrar informe"
              className="text-claridata-textoSecundario transition-colors hover:text-claridata-texto"
            >
              ✏️
            </button>
          )}
        </div>
      </div>

      {errorRenombrar && (
        <p className="text-center text-sm font-medium text-red-400">
          {errorRenombrar}
        </p>
      )}

      <div className="grid grid-cols-2 gap-4 md:grid-cols-3">
        <DatoResumen
          etiqueta="Filas"
          valor={metadatos?.numero_filas.toLocaleString("es-CO") ?? "—"}
        />
        <DatoResumen
          etiqueta="Columnas"
          valor={metadatos?.numero_columnas.toLocaleString("es-CO") ?? "—"}
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

      {informe.descubrimientos && informe.descubrimientos.length >= 0 && (
        <div className="rounded-2xl border border-white/10 bg-white/[0.02] px-6 py-6">
          <SeccionDescubrimientos
            descubrimientos={informe.descubrimientos}
          />
        </div>
      )}

      <p className="text-center text-sm text-claridata-textoSecundario">
        Análisis realizado el {formatearFecha(informe.fecha_creacion)}
      </p>

      {alAnalizarOtro && (
        <button
          type="button"
          onClick={alAnalizarOtro}
          className="mx-auto rounded-full border border-white/15 px-6 py-3 text-sm font-medium text-claridata-textoSecundario transition-colors duration-300 hover:border-white/30 hover:text-claridata-texto"
        >
          Analizar otro archivo
        </button>
      )}

      <ModalRenombrarInforme
        abierto={modalAbierto}
        tituloActual={informe.titulo}
        cargando={renombrando}
        alCerrar={() => setModalAbierto(false)}
        alConfirmar={manejarConfirmarRenombrar}
      />
    </div>
  );
}