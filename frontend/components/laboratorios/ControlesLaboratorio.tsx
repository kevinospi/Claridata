interface PropiedadesControlesLaboratorio {
  cantidadPuntos: number;
  alAgregarPunto: () => void;
}

export function ControlesLaboratorio({
  cantidadPuntos,
  alAgregarPunto,
}: PropiedadesControlesLaboratorio) {
  return (
    <div className="flex items-center gap-3">
      <button
        type="button"
        onClick={alAgregarPunto}
        disabled={cantidadPuntos >= 20}
        className="flex items-center gap-2 rounded-full border border-white/15 px-4 py-2 text-sm font-medium text-claridata-textoSecundario transition-all duration-200 hover:border-claridata-marca/50 hover:text-claridata-texto disabled:cursor-not-allowed disabled:opacity-40"
      >
        <span className="text-base leading-none">+</span>
        Agregar dato
      </button>

      <span className="text-xs text-claridata-textoSecundario">
        {cantidadPuntos} {cantidadPuntos === 1 ? "dato" : "datos"}
      </span>
    </div>
  );
}