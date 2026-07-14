import { PaginaAprender } from "@/components/aprender/PaginaAprender";
import { GuardAutenticacion } from "@/components/auth/GuardAutenticacion";

export default function RutaAprender() {
  return (
    <GuardAutenticacion>
      <PaginaAprender />
    </GuardAutenticacion>
  );
}