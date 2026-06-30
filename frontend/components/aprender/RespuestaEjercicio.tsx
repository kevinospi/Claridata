interface PropiedadesRespuestaEjercicio {
  esCorrecta: boolean;
  explicacion: string;
}

export function RespuestaEjercicio({
  esCorrecta,
  explicacion,
}: PropiedadesRespuestaEjercicio) {
  return (
    <div
      className={`flex flex-col gap-2 rounded-xl border px-5 py-4 ${
        esCorrecta
          ? "border-emerald-400/30 bg-emerald-400/5"
          : "border-red-400/30 bg-red-400/5"
      }`}
    >
      <p
        className={`text-sm font-semibold ${
          esCorrecta ? "text-emerald-300" : "text-red-300"
        }`}
      >
        {esCorrecta ? "¡Correcto! 🎉" : "No es correcto, pero sigue así 💡"}
      </p>
      <p className="text-sm text-claridata-textoSecundario">{explicacion}</p>
    </div>
  );
}