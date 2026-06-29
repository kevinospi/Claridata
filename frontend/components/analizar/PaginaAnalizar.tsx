"use client";

import { useState } from "react";
import { EncabezadoApp } from "@/components/compartidos/EncabezadoApp";
import { ZonaCargaArchivo } from "./ZonaCargaArchivo";
import { TarjetaArchivoSeleccionado } from "./TarjetaArchivoSeleccionado";
import { PantallaCargaAnalisis } from "./PantallaCargaAnalisis";
import { PlaceholderResultado } from "./PlaceholderResultado";
import { ArchivoSeleccionado, EstadoAnalisis } from "@/tipos/analisis";

function obtenerExtension(nombreArchivo: string): string {
  const partes = nombreArchivo.split(".");
  return partes.length > 1 ? partes[partes.length - 1] : "";
}

export function PaginaAnalizar() {
  const [estado, setEstado] = useState<EstadoAnalisis>("idle");
  const [archivo, setArchivo] = useState<ArchivoSeleccionado | null>(null);

  const manejarSeleccionArchivo = (archivoNativo: File) => {
    setArchivo({
      nombre: archivoNativo.name,
      tamañoBytes: archivoNativo.size,
      extension: obtenerExtension(archivoNativo.name),
    });
    setEstado("selected");
  };

  const manejarQuitarArchivo = () => {
    setArchivo(null);
    setEstado("idle");
  };

  const manejarAnalizar = () => {
    setEstado("loading");
  };

  const manejarFinCarga = () => {
    setEstado("result");
  };

  const manejarReiniciar = () => {
    setArchivo(null);
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
            <TarjetaArchivoSeleccionado
              archivo={archivo}
              alQuitarArchivo={manejarQuitarArchivo}
              alAnalizar={manejarAnalizar}
            />
          )}

          {estado === "loading" && (
            <PantallaCargaAnalisis alFinalizar={manejarFinCarga} />
          )}

          {estado === "result" && (
            <PlaceholderResultado alReiniciar={manejarReiniciar} />
          )}
        </div>
      </div>
    </main>
  );
}