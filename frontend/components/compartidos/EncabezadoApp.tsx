"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";

interface PropiedadesEncabezadoApp {
  accionesDerecha?: React.ReactNode;
}

export function EncabezadoApp({ accionesDerecha }: PropiedadesEncabezadoApp) {
  const router = useRouter();

  return (
    <header className="flex w-full items-center justify-between border-b border-white/10 px-6 py-4 md:px-10">
      <div className="relative h-auto w-[140px]">
        <Image
          src="/logo_claridata.png"
          alt="Claridata"
          width={1200}
          height={300}
          className="h-auto w-full"
        />
      </div>

      <div className="flex items-center gap-4">
        {accionesDerecha}

        <button
          type="button"
          onClick={() => router.push("/")}
          className="rounded-full border border-white/15 px-4 py-2 text-sm font-medium text-claridata-textoSecundario transition-colors duration-300 hover:border-white/30 hover:text-claridata-texto"
        >
          ← Volver
        </button>
      </div>
    </header>
  );
}