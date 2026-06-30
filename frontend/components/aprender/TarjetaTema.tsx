"use client";

import { useRouter } from "next/navigation";
import { Tema } from "@/tipos/aprendizaje";

const COLOR_DIFICULTAD: Record<Tema["dificultad"], string> = {
  Principiante: "text-emerald-300 border-emerald-400/30 bg-emerald-400/10",
  Intermedio: "text-claridata-acento border-claridata-acento/30 bg-claridata-acento/10",
  Avanzado: "text-orange-300 border-orange-400/30 bg-orange-400/10",
};

interface PropiedadesTarjetaTema {
  tema: Tema;
}

export function TarjetaTema({ tema }: PropiedadesTarjetaTema) {
  const router = useRouter();

  return (
    <button
      type="button"
      onClick={() => router.push(`/aprender/${tema.id}`)}
      className="flex flex-col items-start gap-4 rounded-2xl border border-white/10 bg-white/[0.03] px-6 py-6 text-left transition-all duration-300 hover:scale-[1.02] hover:border-claridata-marca/40 hover:bg-white/[0.05]"
    >
      <h3 className="text-lg font-semibold text-claridata-texto">
        {tema.nombre}
      </h3>

      <p className="text-sm text-claridata-textoSecundario">
        {tema.descripcion}
      </p>

      <div className="flex items-center gap-2">
        <span
          className={`rounded-full border px-3 py-1 text-xs font-medium ${COLOR_DIFICULTAD[tema.dificultad]}`}
        >
          {tema.dificultad}
        </span>
        <span className="text-xs text-claridata-textoSecundario">
          ⏱ {tema.tiempoLectura}
        </span>
      </div>
    </button>
  );
}