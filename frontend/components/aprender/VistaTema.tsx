"use client";

import { useRouter } from "next/navigation";
import { Tema } from "@/tipos/aprendizaje";
import { Concepto } from "./Concepto";
import { EjercicioInteractivo } from "./EjercicioInteractivo";

const COLOR_DIFICULTAD: Record<Tema["dificultad"], string> = {
  Principiante: "text-emerald-300 border-emerald-400/30 bg-emerald-400/10",
  Intermedio: "text-claridata-acento border-claridata-acento/30 bg-claridata-acento/10",
  Avanzado: "text-orange-300 border-orange-400/30 bg-orange-400/10",
};

interface PropiedadesVistaTema {
  tema: Tema;
}

export function VistaTema({ tema }: PropiedadesVistaTema) {
  const router = useRouter();

  return (
    <div className="flex w-full flex-col gap-10">
      <div className="flex flex-col gap-4 text-center">
        <button
          type="button"
          onClick={() => router.push("/aprender")}
          className="mx-auto text-sm text-claridata-textoSecundario transition-colors hover:text-claridata-texto"
        >
          ← Volver a Aprender
        </button>

        <h1 className="text-3xl font-extrabold tracking-tight text-claridata-texto md:text-4xl">
          {tema.nombre}
        </h1>

        <div className="flex items-center justify-center gap-2">
          <span
            className={`rounded-full border px-3 py-1 text-xs font-medium ${COLOR_DIFICULTAD[tema.dificultad]}`}
          >
            {tema.dificultad}
          </span>
          <span className="text-xs text-claridata-textoSecundario">
            ⏱ {tema.tiempoLectura}
          </span>
        </div>
      </div>

      <Concepto titulo="¿Qué es?">
        <p>{tema.contenido.queEs}</p>
      </Concepto>

      <Concepto titulo="¿Para qué sirve?">
        <p>{tema.contenido.paraQueSirve}</p>
      </Concepto>

      <Concepto titulo="¿Cuándo usarla?">
        <p>{tema.contenido.cuandoUsarla}</p>
      </Concepto>

      <Concepto titulo="¿Cuándo NO usarla?">
        <p>{tema.contenido.cuandoNoUsarla}</p>
      </Concepto>

      <Concepto titulo="Ejemplo sencillo">
        <p>{tema.contenido.ejemplo}</p>
      </Concepto>

      <Concepto titulo="Errores comunes">
        <ul className="flex flex-col gap-2">
          {tema.contenido.erroresComunes.map((error, indice) => (
            <li key={indice} className="flex gap-2">
              <span className="text-red-400">•</span>
              <span>{error}</span>
            </li>
          ))}
        </ul>
      </Concepto>

      <Concepto titulo="Conceptos relacionados">
        <div className="flex flex-wrap gap-2">
          {tema.contenido.conceptosRelacionados.map((concepto) => (
            <span
              key={concepto}
              className="rounded-full border border-white/15 px-3 py-1 text-sm text-claridata-textoSecundario"
            >
              {concepto}
            </span>
          ))}
        </div>
      </Concepto>

      {tema.ejercicios.length > 0 && (
        <section className="flex flex-col gap-4">
          <h2 className="text-xl font-semibold text-claridata-texto">
            Ponlo a prueba
          </h2>
          {tema.ejercicios.map((ejercicio) => (
            <EjercicioInteractivo key={ejercicio.id} ejercicio={ejercicio} />
          ))}
        </section>
      )}
    </div>
  );
}