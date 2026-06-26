import Image from "next/image";

export function EncabezadoBienvenida() {
  return (
    <div className="flex flex-col items-center gap-5 px-6 py-12 text-center">
      <div
        className="flex items-center gap-3 opacity-0"
        style={{ animation: "aparicion-suave 700ms ease-out 0ms forwards" }}
      >
        <Image
          src="/logo_claridata.png"
          alt="Claridata"
          width={56}
          height={56}
          priority
        />
        <span className="text-3xl font-extrabold tracking-tight text-claridata-texto">
          Claridata
        </span>
      </div>

      <h1
        className="max-w-3xl text-4xl font-bold tracking-tight text-claridata-texto opacity-0 md:text-6xl"
        style={{ animation: "aparicion-suave 700ms ease-out 250ms forwards" }}
      >
        Hola, ¿qué deseas hacer hoy?
      </h1>

      <p
        className="max-w-2xl text-lg italic text-claridata-textoSecundario opacity-0 md:text-xl"
        style={{ animation: "aparicion-suave 700ms ease-out 500ms forwards" }}
      >
        Analizar datos y comprender sus resultados nunca había sido tan
        fácil... hasta ahora.
      </p>
    </div>
  );
}