"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { InformeDetalleRespuesta } from "@/tipos/api";
import { renombrarInforme } from "@/lib/api/informes";

import { HeroInforme } from "./secciones/HeroInforme";
import { KpisInforme } from "./secciones/KpisInforme";
import { ResumenEjecutivo } from "./secciones/ResumenEjecutivo";
import { DescubrimientosDashboard } from "./secciones/DescubrimientosDashboard";
import { InterpretacionDashboard } from "./secciones/InterpretacionDashboard";
import { RecomendacionesDashboard } from "./secciones/RecomendacionesDashboard";
import { EstadisticasDescriptivas } from "./secciones/EstadisticasDescriptivas";
import { CorrelacionesDashboard } from "./secciones/CorrelacionesDashboard";
import { OutliersDashboard } from "./secciones/OutliersDashboard";
import { ModalRenombrarInforme } from "./ModalRenombrarInforme";
import { TabsInforme, TabDefinicion } from "./TabsInforme";
import { RenderizadorGraficas } from "./graficas/RenderizadorGraficas";

interface PropiedadesVistaInforme {
  informe: InformeDetalleRespuesta;
  alActualizarInforme?: (informe: InformeDetalleRespuesta) => void;
  alAnalizarOtro?: () => void;
}

type IdTab =
  | "resumen"
  | "descubrimientos"
  | "interpretacion"
  | "recomendaciones"
  | "estadisticas"
  | "correlaciones"
  | "outliers"
  | "graficas";

const TABS: TabDefinicion[] = [
  { id: "resumen", etiqueta: "Resumen", emoji: "📋", disponible: true },
  { id: "descubrimientos", etiqueta: "Descubrimientos", emoji: "🔍", disponible: true },
  { id: "interpretacion", etiqueta: "Interpretación", emoji: "🧠", disponible: true },
  { id: "recomendaciones", etiqueta: "Recomendaciones", emoji: "💡", disponible: true },
  { id: "estadisticas", etiqueta: "Estadísticas", emoji: "📊", disponible: true },
  { id: "correlaciones", etiqueta: "Correlaciones", emoji: "🔗", disponible: true },
  { id: "outliers", etiqueta: "Outliers", emoji: "⚠️", disponible: true },
  { id: "graficas", etiqueta: "Gráficas", emoji: "📈", disponible: true },
];

const variantes = {
  entrada: { opacity: 0, y: 10 },
  visible: { opacity: 1, y: 0 },
  salida: { opacity: 0, y: -6 },
};

export function VistaInforme({
  informe: informeInicial,
  alActualizarInforme,
  alAnalizarOtro,
}: PropiedadesVistaInforme) {
  const [informe, setInforme] = useState(informeInicial);
  const [tabActiva, setTabActiva] = useState<IdTab>("resumen");
  const [modalAbierto, setModalAbierto] = useState(false);
  const [renombrando, setRenombrando] = useState(false);
  const [errorRenombrar, setErrorRenombrar] = useState<string | null>(null);

  const manejarConfirmarRenombrar = async (nuevoTitulo: string) => {
    setRenombrando(true);
    setErrorRenombrar(null);
    try {
      const actualizado = await renombrarInforme(informe.id, nuevoTitulo);
      setInforme(actualizado);
      alActualizarInforme?.(actualizado);
      setModalAbierto(false);
    } catch {
      setErrorRenombrar("No fue posible renombrar el informe. Intenta de nuevo.");
    } finally {
      setRenombrando(false);
    }
  };

  return (
    <div className="flex w-full flex-col gap-6">
      <HeroInforme
        informe={informe}
        alRenombrar={alActualizarInforme ? () => setModalAbierto(true) : undefined}
      />

      <KpisInforme informe={informe} />

      <TabsInforme
        tabs={TABS}
        tabActiva={tabActiva}
        alCambiarTab={(id) => setTabActiva(id as IdTab)}
      />

      <AnimatePresence mode="wait">
        <motion.div
          key={tabActiva}
          variants={variantes}
          initial="entrada"
          animate="visible"
          exit="salida"
          transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
          className="rounded-2xl border border-white/10 bg-white/[0.02] px-6 py-6"
        >
          {tabActiva === "resumen" && (
            <ResumenEjecutivo informe={informe} />
          )}
          {tabActiva === "descubrimientos" && (
            <DescubrimientosDashboard
              descubrimientos={informe.descubrimientos ?? []}
            />
          )}
          {tabActiva === "interpretacion" && (
            <InterpretacionDashboard
              secciones={informe.interpretacion_profesional ?? []}
            />
          )}
          {tabActiva === "recomendaciones" && (
            <RecomendacionesDashboard
              recomendaciones={informe.recomendaciones_inteligentes ?? []}
            />
          )}
          {tabActiva === "estadisticas" && (
            <EstadisticasDescriptivas informe={informe} />
          )}
          {tabActiva === "correlaciones" && (
            <CorrelacionesDashboard informe={informe} />
          )}
          {tabActiva === "outliers" && (
            <OutliersDashboard informe={informe} />
          )}
          {tabActiva === "graficas" && (
            <RenderizadorGraficas
            visualizaciones={informe.visualizaciones_inteligentes ?? []}
  />
)}
        </motion.div>
      </AnimatePresence>

      {errorRenombrar && (
        <p className="text-center text-sm font-medium text-red-400">
          {errorRenombrar}
        </p>
      )}

      {alAnalizarOtro && (
        <button
          type="button"
          onClick={alAnalizarOtro}
          className="mx-auto rounded-full border border-white/15 px-6 py-3 text-sm font-medium text-claridata-textoSecundario transition-colors duration-300 hover:border-white/30 hover:text-claridata-texto"
        >
          Analizar otro archivo
        </button>
      )}

      <ModalRenombrarInforme
        abierto={modalAbierto}
        tituloActual={informe.titulo}
        cargando={renombrando}
        alCerrar={() => setModalAbierto(false)}
        alConfirmar={manejarConfirmarRenombrar}
      />
    </div>
  );
}