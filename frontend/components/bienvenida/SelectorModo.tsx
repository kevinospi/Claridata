"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { TarjetaModo } from "./TarjetaModo";
import { MODOS } from "@/lib/constantes/modos";
import { IdModo } from "@/tipos/modo";

export function SelectorModo() {
  const router = useRouter();
  const [modoEnHover, setModoEnHover] = useState<IdModo | null>(null);
  const [modoSeleccionado, setModoSeleccionado] = useState<IdModo | null>(
    null,
  );
  const [expansionActiva, setExpansionActiva] = useState(false);

  const manejarSeleccion = (modo: IdModo, ruta: string) => {
    if (modoSeleccionado) return;

    setModoSeleccionado(modo);

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        setExpansionActiva(true);
      });
    });

    window.setTimeout(() => {
      router.push(ruta);
    }, 700);
  };

  return (
    <div className="flex w-full flex-1 flex-col">
      {MODOS.map((modo) => (
        <TarjetaModo
          key={modo.id}
          modo={modo}
          estaEnHover={modoEnHover === modo.id && modoSeleccionado === null}
          estaExpandiendo={expansionActiva && modoSeleccionado === modo.id}
          estaDesapareciendo={
            expansionActiva &&
            modoSeleccionado !== null &&
            modoSeleccionado !== modo.id
          }
          alIniciarHover={() => setModoEnHover(modo.id)}
          alFinalizarHover={() => setModoEnHover(null)}
          alSeleccionar={() => manejarSeleccion(modo.id, modo.ruta)}
        />
      ))}
    </div>
  );
}