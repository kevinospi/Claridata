"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";
import { useCerrarSesion } from "@/hooks/useAuth";
import { haySesionActiva } from "@/lib/auth/sesion";
import { useEffect, useState } from "react";

interface PropiedadesEncabezadoApp {
  accionesDerecha?: React.ReactNode;
}

export function EncabezadoApp({ accionesDerecha }: PropiedadesEncabezadoApp) {
  const router = useRouter();
  const cerrarSesion = useCerrarSesion();
  const [sesionActiva, setSesionActiva] = useState(false);

  useEffect(() => {
    setSesionActiva(haySesionActiva());
  }, []);

  return (
    <header className="flex w-full items-center justify-between border-b border-white/10 px-6 py-4 md:px-10">
      <button
        type="button"
        onClick={() => router.push("/")}
        className="relative h-auto w-[140px]"
        aria-label="Ir al inicio"
      >
        <Image
          src="/logo_claridata.png"
          alt="Claridata"
          width={1200}
          height={300}
          className="h-auto w-full"
        />
      </button>

      <div className="flex items-center gap-3">
        {sesionActiva && (
          <button
            type="button"
            onClick={() => router.push("/informes")}
            className="rounded-full border border-white/15 px-4 py-2 text-sm font-medium text-claridata-textoSecundario transition-colors duration-300 hover:border-white/30 hover:text-claridata-texto"
          >
            Mis informes
          </button>
        )}

        {accionesDerecha}

        <button
          type="button"
          onClick={() => router.push("/")}
          className="rounded-full border border-white/15 px-4 py-2 text-sm font-medium text-claridata-textoSecundario transition-colors duration-300 hover:border-white/30 hover:text-claridata-texto"
        >
          ← Volver
        </button>

        {sesionActiva && (
          <button
            type="button"
            onClick={cerrarSesion}
            className="rounded-full border border-red-400/20 px-4 py-2 text-sm font-medium text-red-400/70 transition-colors duration-300 hover:border-red-400/50 hover:text-red-400"
          >
            Cerrar sesión
          </button>
        )}
      </div>
    </header>
  );
}