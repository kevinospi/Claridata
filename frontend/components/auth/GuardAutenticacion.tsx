"use client";

import { useAuth } from "@/hooks/useAuth";

interface PropiedadesGuardAutenticacion {
  children: React.ReactNode;
}

export function GuardAutenticacion({
  children,
}: PropiedadesGuardAutenticacion) {
  const estado = useAuth();

  if (estado === "verificando") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-claridata-fondo">
        <div className="relative h-10 w-10">
          <div className="absolute inset-0 rounded-full border-4 border-white/10" />
          <div className="absolute inset-0 animate-spin rounded-full border-4 border-transparent border-t-claridata-marca" />
        </div>
      </div>
    );
  }

  if (estado === "no_autenticado") {
    return null;
  }

  return <>{children}</>;
}