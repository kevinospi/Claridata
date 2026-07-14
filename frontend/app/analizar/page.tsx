import { PaginaAnalizar } from "@/components/analizar/PaginaAnalizar";
import { GuardAutenticacion } from "@/components/auth/GuardAutenticacion";

export default function RutaAnalizar() {
  return (
    <GuardAutenticacion>
      <PaginaAnalizar />
    </GuardAutenticacion>
  );
}