interface PropiedadesMensajeErrorAnalisis {
  mensaje: string;
  alReintentar?: () => void;
}

export function MensajeErrorAnalisis({
  mensaje,
  alReintentar,
}: PropiedadesMensajeErrorAnalisis) {
  return (
    <div className="flex w-full flex-col items-center gap-4 rounded-2xl border border-red-400/30 bg-red-400/5 px-6 py-8 text-center">
      <div className="text-4xl">⚠️</div>

      <p className="max-w-md text-base font-medium text-red-300">
        {mensaje}
      </p>

      {alReintentar && (
        <button
          type="button"
          onClick={alReintentar}
          className="rounded-full border border-red-400/40 px-5 py-2 text-sm font-medium text-red-300 transition-colors duration-300 hover:border-red-400 hover:text-red-200"
        >
          Intentar de nuevo
        </button>
      )}
    </div>
  );
}