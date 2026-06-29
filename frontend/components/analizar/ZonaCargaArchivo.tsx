"use client";

import { useRef, useState } from "react";

const EXTENSIONES_PERMITIDAS = [".csv", ".xlsx"];

interface PropiedadesZonaCargaArchivo {
  alSeleccionarArchivo: (archivo: File) => void;
}

function obtenerExtension(nombreArchivo: string): string {
  const partes = nombreArchivo.toLowerCase().split(".");
  return partes.length > 1 ? `.${partes[partes.length - 1]}` : "";
}

function esExtensionValida(nombreArchivo: string): boolean {
  return EXTENSIONES_PERMITIDAS.includes(obtenerExtension(nombreArchivo));
}

export function ZonaCargaArchivo({
  alSeleccionarArchivo,
}: PropiedadesZonaCargaArchivo) {
  const [estaArrastrando, setEstaArrastrando] = useState(false);
  const [errorArchivo, setErrorArchivo] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const procesarArchivo = (archivo: File) => {
    if (!esExtensionValida(archivo.name)) {
      setErrorArchivo(
        "Solo se aceptan archivos con extensión .csv o .xlsx.",
      );
      return;
    }

    setErrorArchivo(null);
    alSeleccionarArchivo(archivo);
  };

  const manejarDrop = (evento: React.DragEvent<HTMLDivElement>) => {
    evento.preventDefault();
    setEstaArrastrando(false);

    const archivo = evento.dataTransfer.files?.[0];
    if (archivo) {
      procesarArchivo(archivo);
    }
  };

  const manejarSeleccionInput = (
    evento: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const archivo = evento.target.files?.[0];
    if (archivo) {
      procesarArchivo(archivo);
    }
    evento.target.value = "";
  };

  return (
    <div className="flex w-full flex-col gap-3">
      <div
        onDragOver={(evento) => {
          evento.preventDefault();
          setEstaArrastrando(true);
        }}
        onDragLeave={() => setEstaArrastrando(false)}
        onDrop={manejarDrop}
        className={`
          flex w-full flex-col items-center justify-center gap-5
          rounded-3xl border-2 border-dashed px-10 py-20
          text-center transition-all duration-300
          ${
            estaArrastrando
              ? "border-claridata-marca bg-claridata-marca/5 scale-[1.01]"
              : "border-white/15 bg-white/[0.02]"
          }
        `}
      >
        <div className="text-6xl">📂</div>

        <div>
          <p className="text-xl font-semibold text-claridata-texto">
            Arrastra aquí tu archivo
          </p>
          <p className="mt-1 text-claridata-textoSecundario">o</p>
        </div>

        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          className="rounded-full bg-claridata-marca px-6 py-3 text-sm font-semibold text-[#022C33] transition-transform duration-300 hover:scale-[1.03]"
        >
          Seleccionar archivo
        </button>

        <p className="text-sm text-claridata-textoSecundario">
          Selecciona uno desde tu computador
        </p>

        <p className="text-xs uppercase tracking-wide text-claridata-textoSecundario/70">
          Formatos soportados: CSV · XLSX
        </p>

        <input
          ref={inputRef}
          type="file"
          accept={EXTENSIONES_PERMITIDAS.join(",")}
          onChange={manejarSeleccionInput}
          className="hidden"
        />
      </div>

      {errorArchivo && (
        <p className="text-center text-sm font-medium text-red-400">
          {errorArchivo}
        </p>
      )}
    </div>
  );
}