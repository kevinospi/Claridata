import { ArchivoSeleccionado } from "@/tipos/analisis";

interface PropiedadesTarjetaArchivoSeleccionado {
  archivo: ArchivoSeleccionado;
  alQuitarArchivo: () => void;
  alAnalizar: () => void;
}

function formatearTamaño(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function TarjetaArchivoSeleccionado({
  archivo,
  alQuitarArchivo,
  alAnalizar,
}: PropiedadesTarjetaArchivoSeleccionado) {
  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/[0.03] px-6 py-5">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-claridata-marca/10 text-2xl">
            📄
          </div>
          <div className="text-left">
            <p className="font-medium text-claridata-texto">
              {archivo.nombre}
            </p>
            <p className="text-sm text-claridata-textoSecundario">
              {formatearTamaño(archivo.tamañoBytes)} ·{" "}
              {archivo.extension.toUpperCase()}
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={alQuitarArchivo}
          aria-label="Quitar archivo"
          className="text-claridata-textoSecundario transition-colors hover:text-claridata-texto"
        >
          ✕
        </button>
      </div>

      <button
        type="button"
        onClick={alAnalizar}
        className="w-full rounded-full bg-claridata-marca py-4 text-base font-semibold text-[#022C33] transition-transform duration-300 hover:scale-[1.01]"
      >
        Analizar Dataset
      </button>
    </div>
  );
}