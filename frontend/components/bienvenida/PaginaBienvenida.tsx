"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { EncabezadoBienvenida } from "./EncabezadoBienvenida";
import { SelectorModo } from "./SelectorModo";
import { haySesionActiva } from "@/lib/auth/sesion";

export function PaginaBienvenida() {
  const router = useRouter();
  const [sesion, setSesion] = useState<boolean | null>(null);

  useEffect(() => {
    setSesion(haySesionActiva());
  }, []);

  if (sesion === null) {
    return (
      <main className="flex h-screen w-full items-center justify-center bg-claridata-fondo">
        <div className="relative h-10 w-10">
          <div className="absolute inset-0 rounded-full border-4 border-white/10" />
          <div className="absolute inset-0 animate-spin rounded-full border-4 border-transparent border-t-claridata-marca" />
        </div>
      </main>
    );
  }

  if (!sesion) {
    return (
      <main className="flex h-screen w-full flex-col items-center justify-center gap-8 bg-claridata-fondo px-6">
        <EncabezadoBienvenida />
        <div className="flex gap-4">
          <button
            type="button"
            onClick={() => router.push("/login")}
            className="rounded-full border border-claridata-marca px-6 py-3 text-sm font-semibold text-claridata-marca transition-all hover:bg-claridata-marca hover:text-[#022C33]"
          >
            Iniciar sesión
          </button>
          <button
            type="button"
            onClick={() => router.push("/registro")}
            className="rounded-full bg-claridata-marca px-6 py-3 text-sm font-semibold text-[#022C33] transition-transform hover:scale-[1.02]"
          >
            Crear cuenta
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="flex h-screen w-full flex-col bg-claridata-fondo">
      <EncabezadoBienvenida />
      <SelectorModo />
    </main>
  );
}