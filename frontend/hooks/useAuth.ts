"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { haySesionActiva, cerrarSesion } from "@/lib/auth/sesion";

export type EstadoAuth = "verificando" | "autenticado" | "no_autenticado";

export function useAuth(): EstadoAuth {
  const router = useRouter();
  const [estado, setEstado] = useState<EstadoAuth>("verificando");

  useEffect(() => {
    if (haySesionActiva()) {
      setEstado("autenticado");
    } else {
      setEstado("no_autenticado");
      router.replace("/login");
    }
  }, [router]);

  return estado;
}

export function useCerrarSesion(): () => void {
  const router = useRouter();

  return () => {
    cerrarSesion();
    router.replace("/login");
  };
}