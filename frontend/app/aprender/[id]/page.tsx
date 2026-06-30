import { notFound } from "next/navigation";
import { VistaTema } from "@/components/aprender/VistaTema";
import { EncabezadoApp } from "@/components/compartidos/EncabezadoApp";
import { obtenerTemaPorId } from "@/lib/aprendizaje/indice";

interface PropiedadesPagina {
  params: Promise<{ id: string }>;
}

export default async function RutaTemaAprender({
  params,
}: PropiedadesPagina) {
  const { id } = await params;
  const tema = obtenerTemaPorId(id);

  if (!tema) {
    notFound();
  }

  return (
    <main className="flex min-h-screen w-full flex-col bg-claridata-fondo">
      <EncabezadoApp />

      <div className="flex flex-1 justify-center px-6 py-16 md:px-10">
        <div className="w-full max-w-2xl">
          <VistaTema tema={tema} />
        </div>
      </div>
    </main>
  );
}