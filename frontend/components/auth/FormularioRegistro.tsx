"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { registrarUsuario } from "@/lib/api/auth";
import { iniciarSesion } from "@/lib/api/auth";
import { ErrorApiRespuesta, ErrorRed } from "@/lib/api/cliente";

export function FormularioRegistro() {
  const router = useRouter();
  const [nombre, setNombre] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const manejarEnvio = async () => {
    if (!nombre.trim() || !email.trim() || !password.trim()) {
      setError("Completa todos los campos.");
      return;
    }

    if (password.length < 8) {
      setError("La contraseña debe tener al menos 8 caracteres.");
      return;
    }

    setCargando(true);
    setError(null);

    try {
      await registrarUsuario({
        nombre: nombre.trim(),
        email: email.trim(),
        password,
      });
      await iniciarSesion({ email: email.trim(), password });
      router.replace("/");
    } catch (err) {
      if (err instanceof ErrorApiRespuesta && err.codigoEstado === 409) {
        setError("Ya existe una cuenta con ese email.");
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
          Nombre
        </label>
        <input
          type="text"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          placeholder="Tu nombre"
          className="rounded-xl border border-white/15 bg-white/[0.03] px-4 py-3 text-claridata-texto outline-none transition-colors focus:border-claridata-marca"
        />
      </div>

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
          placeholder="Mínimo 8 caracteres"
          className="rounded-xl border border-white/15 bg-white/[0.03] px-4 py-3 text-claridata-texto outline-none transition-colors focus:border-claridata-marca"
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
        {cargando ? "Creando cuenta..." : "Crear cuenta"}
      </button>

      <p className="text-center text-sm text-claridata-textoSecundario">
        ¿Ya tienes cuenta?{" "}
        <button
          type="button"
          onClick={() => router.push("/login")}
          className="font-medium text-claridata-marca hover:underline"
        >
          Inicia sesión
        </button>
      </p>
    </div>
  );
}