"use client";

import { motion } from "framer-motion";

export interface TabDefinicion {
  id: string;
  etiqueta: string;
  emoji: string;
  disponible: boolean;
}

interface PropiedadesTabsInforme {
  tabs: TabDefinicion[];
  tabActiva: string;
  alCambiarTab: (id: string) => void;
}

export function TabsInforme({
  tabs,
  tabActiva,
  alCambiarTab,
}: PropiedadesTabsInforme) {
  return (
    <div className="scrollbar-hide flex gap-1 overflow-x-auto rounded-2xl border border-white/10 bg-white/[0.02] p-1.5">
      {tabs.map((tab) => {
        const activa = tabActiva === tab.id;
        return (
          <button
            key={tab.id}
            type="button"
            onClick={() => tab.disponible && alCambiarTab(tab.id)}
            disabled={!tab.disponible}
            className="relative flex shrink-0 items-center gap-1.5 rounded-xl px-4 py-2.5 text-sm font-medium transition-colors"
            style={{
              color: activa
                ? "#22D3EE"
                : tab.disponible
                  ? "#94A3B8"
                  : "#475569",
              cursor: tab.disponible ? "pointer" : "not-allowed",
            }}
          >
            {activa && (
              <motion.div
                layoutId="tab-activa"
                className="absolute inset-0 rounded-xl bg-claridata-marca/10"
                style={{ border: "1px solid rgba(34,211,238,0.25)" }}
                transition={{ type: "spring", duration: 0.4, bounce: 0.15 }}
              />
            )}
            <span className="relative z-10">{tab.emoji}</span>
            <span className="relative z-10 whitespace-nowrap">{tab.etiqueta}</span>
          </button>
        );
      })}
    </div>
  );
}