import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        claridata: {
          fondo: "#0B1120",
          marca: "#22D3EE",
          marcaSecundario: "#67E8F9",
          acento: "#FDE68A",
          texto: "#FFFFFF",
          textoSecundario: "#94A3B8",
          superficie: "#111827",
          superficieElevada: "#1A2333",
        },
      },
      fontFamily: {
        sans: ["var(--font-claridata)", "system-ui", "sans-serif"],
      },
      transitionTimingFunction: {
        "claridata-expo": "cubic-bezier(0.16, 1, 0.3, 1)",
      },
      boxShadow: {
        "claridata-suave": "0 8px 30px -8px rgba(34, 211, 238, 0.25)",
        "claridata-hover": "0 12px 40px -6px rgba(34, 211, 238, 0.4)",
      },
    },
  },
  plugins: [],
};

export default config;