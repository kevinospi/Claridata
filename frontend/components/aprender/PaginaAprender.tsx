import { EncabezadoApp } from "@/components/compartidos/EncabezadoApp";
import { TarjetaTema } from "./TarjetaTema";
import { TEMAS } from "@/lib/aprendizaje/indice";

export function PaginaAprender() {
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
              Explora conceptos de estadística y probabilidad a tu propio
              ritmo.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {TEMAS.map((tema) => (
              <TarjetaTema key={tema.id} tema={tema} />
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}