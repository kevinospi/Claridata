import { PaginaInformes } from "@/components/informes/PaginaInformes";
import { GuardAutenticacion } from "@/components/auth/GuardAutenticacion";

export default function RutaInformes() {
  return (
    <GuardAutenticacion>
      <PaginaInformes />
    </GuardAutenticacion>
  );
}