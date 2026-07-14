import Image from "next/image";
import { FormularioLogin } from "@/components/auth/FormularioLogin";

export default function PaginaLogin() {
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
            Bienvenido de vuelta
          </h1>
          <p className="text-sm text-claridata-textoSecundario">
            Inicia sesión para continuar en Claridata.
          </p>
        </div>

        <div className="rounded-2xl border border-white/10 bg-white/[0.02] px-6 py-8">
          <FormularioLogin />
        </div>
      </div>
    </main>
  );
}