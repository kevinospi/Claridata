import Image from "next/image";
import { FormularioRegistro } from "@/components/auth/FormularioRegistro";

export default function PaginaRegistro() {
  return (
    <main className="flex min-h-screen w-full flex-col items-center justify-center bg-claridata-fondo px-6 py-12">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center gap-4">
          <div className="relative h-auto w-[160px]">
            <Image
              src="/logo_claridata.png"
              alt="Claridata"
              width={1200}
              height={300}
              className="h-auto w-full"
              priority
            />
          </div>
          <h1 className="text-2xl font-bold text-claridata-texto">
            Crea tu cuenta
          </h1>
          <p className="text-sm text-claridata-textoSecundario">
            Empieza a aprender y analizar con Claridata.
          </p>
        </div>

        <div className="rounded-2xl border border-white/10 bg-white/[0.02] px-6 py-8">
          <FormularioRegistro />
        </div>
      </div>
    </main>
  );
}