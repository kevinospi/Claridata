interface PropiedadesPlaceholderResultado {
  alReiniciar: () => void;
}

export function PlaceholderResultado({
  alReiniciar,
}: PropiedadesPlaceholderResultado) {
  return (
    <div className="flex flex-col items-center justify-center gap-6 py-24 text-center">
      <div className="text-6xl">✨</div>

      <p className="max-w-md text-xl font-medium text-claridata-texto">
        En la siguiente fase aparecerán aquí los resultados del análisis.
      </p>

      <button
        type="button"
        onClick={alReiniciar}
        className="mt-2 rounded-full border border-white/15 px-6 py-3 text-sm font-medium text-claridata-textoSecundario transition-colors duration-300 hover:border-white/30 hover:text-claridata-texto"
      >
        Analizar otro archivo
      </button>
    </div>
  );
}