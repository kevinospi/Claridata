import { LaboratorioMedia } from "@/components/laboratorios/LaboratorioMedia";
import { EncabezadoApp } from "@/components/compartidos/EncabezadoApp";
import { GuardAutenticacion } from "@/components/auth/GuardAutenticacion";

export default function RutaLaboratorios() {
  return (
    <GuardAutenticacion>
      <main className="flex min-h-screen w-full flex-col bg-claridata-fondo">
        <EncabezadoApp />
        <div className="flex flex-1 justify-center px-6 py-12 md:px-10">
          <div className="w-full max-w-3xl">
            <LaboratorioMedia />
          </div>
        </div>
      </main>
    </GuardAutenticacion>
  );
}