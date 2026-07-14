"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { iniciarSesion } from "@/lib/api/auth";
import { ErrorApiRespuesta, ErrorRed } from "@/lib/api/cliente";

export function FormularioLogin() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const manejarEnvio = async () => {
    if (!email.trim() || !password.trim()) {
      setError("Completa todos los campos.");
      return;
    }

    setCargando(true);
    setError(null);

    try {
      await iniciarSesion({ email: email.trim(), password });
      router.replace("/");
    } catch (err) {
      if (err instanceof ErrorApiRespuesta && err.codigoEstado === 401) {
        setError("Email o contraseña incorrectos.");
      } else if (err instanceof ErrorRed) {
        setError(err.message);
      } else {
        setError("Ocurrió un error inesperado. Intenta de nuevo.");
      }
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="flex flex-col gap-5">
      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-claridata-textoSecundario">
          Email
        </label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="tu@email.com"
          className="rounded-xl border border-white/15 bg-white/[0.03] px-4 py-3 text-claridata-texto outline-none transition-colors focus:border-claridata-marca"
          onKeyDown={(e) => e.key === "Enter" && manejarEnvio()}
        />
      </div>

      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-claridata-textoSecundario">
          Contraseña
        </label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
          className="rounded-xl border border-white/15 bg-white/[0.03] px-4 py-3 text-claridata-texto outline-none transition-colors focus:border-claridata-marca"
          onKeyDown={(e) => e.key === "Enter" && manejarEnvio()}
        />
      </div>

      {error && (
        <p className="rounded-xl border border-red-400/30 bg-red-400/5 px-4 py-3 text-sm text-red-300">
          {error}
        </p>
      )}

      <button
        type="button"
        onClick={manejarEnvio}
        disabled={cargando}
        className="w-full rounded-full bg-claridata-marca py-3 text-sm font-semibold text-[#022C33] transition-transform hover:scale-[1.01] disabled:opacity-50"
      >
        {cargando ? "Iniciando sesión..." : "Iniciar sesión"}
      </button>

      <p className="text-center text-sm text-claridata-textoSecundario">
        ¿No tienes cuenta?{" "}
        <button
          type="button"
          onClick={() => router.push("/registro")}
          className="font-medium text-claridata-marca hover:underline"
        >
          Regístrate
        </button>
      </p>
    </div>
  );
}