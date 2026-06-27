import Image from "next/image";

export function EncabezadoBienvenida() {
  return (
    <div className="flex flex-col items-center gap-8 px-6 py-16 text-center">
      <div
        className="relative h-auto w-[220px] opacity-0 md:w-[280px]"
        style={{ animation: "aparicion-suave 700ms ease-out 0ms forwards" }}
      >
        <Image
          src="/logo_claridata.png"
          alt="Claridata"
          width={1200}
          height={300}
          priority
          className="h-auto w-full"
        />
      </div>

      <h1
        className="max-w-4xl text-5xl font-extrabold leading-tight tracking-tight text-claridata-texto opacity-0 md:text-6xl lg:text-7xl"
        style={{ animation: "aparicion-suave 700ms ease-out 250ms forwards" }}
      >
        Hola, ¿qué deseas hacer hoy?
      </h1>

      <p
        className="max-w-2xl text-lg leading-relaxed text-claridata-textoSecundario opacity-0 md:text-xl"
        style={{ animation: "aparicion-suave 700ms ease-out 500ms forwards" }}
      >
        Analizar datos y comprender sus resultados nunca había sido tan
        fácil... hasta ahora.
      </p>
    </div>
  );
}