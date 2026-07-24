"use client";

import { useState } from "react";
import { EncabezadoApp } from "@/components/compartidos/EncabezadoApp";
import { ZonaCargaArchivo } from "./ZonaCargaArchivo";
import { TarjetaArchivoSeleccionado } from "./TarjetaArchivoSeleccionado";
import { PantallaCargaAnalisis } from "./PantallaCargaAnalisis";
import { MensajeErrorAnalisis } from "./MensajeErrorAnalisis";
import { VistaInforme } from "@/components/informes/VistaInforme";
import { ArchivoSeleccionado, EstadoAnalisis } from "@/tipos/analisis";
import { InformeDetalleRespuesta } from "@/tipos/api";
import {
  analizarDataset,
  obtenerDataset,
  subirDataset,
} from "@/lib/api/datasets";
import { ErrorApiRespuesta, ErrorRed, ErrorSesionExpirada } from "@/lib/api/cliente";


function obtenerExtension(nombreArchivo: string): string {
  const partes = nombreArchivo.split(".");
  return partes.length > 1 ? partes[partes.length - 1] : "";
}

function obtenerMensajeError(error: unknown): string {
  if (error instanceof ErrorSesionExpirada) return error.message;
  if (error instanceof ErrorRed) return error.message;
  if (error instanceof ErrorApiRespuesta) {
    if (error.codigoEstado === 422) return `El archivo no pudo procesarse: ${error.message}`;
    return error.message;
  }
  return "Ocurrió un error inesperado. Intenta de nuevo.";
}

export function PaginaAnalizar() {
  const [estado, setEstado] = useState<EstadoAnalisis>("idle");
  const [archivoNativo, setArchivoNativo] = useState<File | null>(null);
  const [archivo, setArchivo] = useState<ArchivoSeleccionado | null>(null);
  const [informeResultado, setInformeResultado] =
    useState<InformeDetalleRespuesta | null>(null);
  const [mensajeError, setMensajeError] = useState<string | null>(null);

  const manejarSeleccionArchivo = (archivoSeleccionado: File) => {
    setArchivoNativo(archivoSeleccionado);
    setArchivo({
      nombre: archivoSeleccionado.name,
      tamañoBytes: archivoSeleccionado.size,
      extension: obtenerExtension(archivoSeleccionado.name),
    });
    setMensajeError(null);
    setEstado("selected");
  };

  const manejarQuitarArchivo = () => {
    setArchivoNativo(null);
    setArchivo(null);
    setMensajeError(null);
    setEstado("idle");
  };

  const ejecutarAnalisisReal = async () => {
    if (!archivoNativo) return;

    setEstado("loading");
    setMensajeError(null);

    try {
      const dataset = await subirDataset(archivoNativo);
      const informe = await analizarDataset(dataset.id);

      setInformeResultado(informe);
      setEstado("result");
    } catch (error) {
      setMensajeError(obtenerMensajeError(error));
      setEstado("selected");
    }
  };

  const manejarReiniciar = () => {
    setArchivoNativo(null);
    setArchivo(null);
    setInformeResultado(null);
    setMensajeError(null);
    setEstado("idle");
  };

  return (
    <main className="flex min-h-screen w-full flex-col bg-claridata-fondo">
      <EncabezadoApp />

      <div className="flex flex-1 flex-col items-center px-6 py-16 md:px-10">
        <div className="w-full max-w-2xl">
          {estado === "idle" || estado === "selected" ? (
            <div className="mb-12 text-center">
              <h1 className="text-4xl font-extrabold tracking-tight text-claridata-texto md:text-5xl">
                Analiza tus datos
              </h1>
              <p className="mt-4 text-lg text-claridata-textoSecundario">
                Sube un archivo CSV o Excel y deja que Claridata encuentre
                patrones, genere estadísticas e interprete los resultados
                contigo.
              </p>
            </div>
          ) : null}

          {estado === "idle" && (
            <ZonaCargaArchivo alSeleccionarArchivo={manejarSeleccionArchivo} />
          )}

          {estado === "selected" && archivo && (
            <div className="flex flex-col gap-6">
              <TarjetaArchivoSeleccionado
                archivo={archivo}
                alQuitarArchivo={manejarQuitarArchivo}
                alAnalizar={ejecutarAnalisisReal}
              />
              {mensajeError && (
                <MensajeErrorAnalisis
                  mensaje={mensajeError}
                  alReintentar={ejecutarAnalisisReal}
                />
              )}
            </div>
          )}

          {estado === "loading" && <PantallaCargaAnalisis />}

          {estado === "result" && informeResultado && (
            <VistaInforme
              informe={informeResultado}
              alActualizarInforme={setInformeResultado}
              alAnalizarOtro={manejarReiniciar}
            />
          )}
        </div>
      </div>
    </main>
  );
}