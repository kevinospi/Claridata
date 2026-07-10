"use client";

import { useRouter } from "next/navigation";
import { EncabezadoApp } from "@/components/compartidos/EncabezadoApp";
import { TarjetaTema } from "./TarjetaTema";
import { TEMAS } from "@/lib/aprendizaje/indice";

export function PaginaAprender() {
  const router = useRouter();

  return (
    <main className="flex min-h-screen w-full flex-col bg-claridata-fondo">
      <EncabezadoApp />

      <div className="flex flex-1 flex-col items-center px-6 py-16 md:px-10">
        <div className="w-full max-w-4xl">
          <div className="mb-12 text-center">
            <h1 className="text-4xl font-extrabold tracking-tight text-claridata-texto md:text-5xl">
              ¿Qué quieres aprender hoy?
            </h1>
            <p className="mt-4 text-lg text-claridata-textoSecundario">
              Explora conceptos de estadística y probabilidad a tu propio ritmo.
            </p>
          </div>

          <div className="mb-10">
            <p className="mb-4 text-xs font-semibold uppercase tracking-widest text-claridata-marca">
              Laboratorios interactivos
            </p>
            <button
              type="button"
              onClick={() => router.push("/laboratorios")}
              className="flex w-full flex-col gap-3 rounded-2xl border border-claridata-marca/30 bg-claridata-marca/5 px-6 py-6 text-left transition-all duration-300 hover:border-claridata-marca/60 hover:bg-claridata-marca/10"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">🔬</span>
                <span className="text-lg font-semibold text-claridata-texto">
                  Medidas de Tendencia Central
                </span>
                <span className="ml-auto rounded-full border border-claridata-marca/40 px-3 py-1 text-xs font-medium text-claridata-marca">
                  Nuevo
                </span>
              </div>
              <p className="text-sm text-claridata-textoSecundario">
                Arrastra datos, crea outliers y descubre por qué la media puede
                mentirte.
              </p>
            </button>
          </div>

          <div>
            <p className="mb-4 text-xs font-semibold uppercase tracking-widest text-claridata-textoSecundario">
              Lecciones
            </p>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {TEMAS.map((tema) => (
                <TarjetaTema key={tema.id} tema={tema} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}