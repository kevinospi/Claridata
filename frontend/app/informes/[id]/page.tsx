import { PaginaDetalleInforme } from "@/components/informes/PaginaDetalleInforme";
import { GuardAutenticacion } from "@/components/auth/GuardAutenticacion";

interface PropiedadesPagina {
  params: Promise<{ id: string }>;
}

export default async function RutaDetalleInforme({
  params,
}: PropiedadesPagina) {
  const { id } = await params;
  return (
    <GuardAutenticacion>
      <PaginaDetalleInforme informeId={id} />
    </GuardAutenticacion>
  );
}