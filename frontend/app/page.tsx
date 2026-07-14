import { PaginaBienvenida } from "@/components/bienvenida/PaginaBienvenida";
import { GuardAutenticacion } from "@/components/auth/GuardAutenticacion";

export default function Inicio() {
  return (
    <GuardAutenticacion>
      <PaginaBienvenida />
    </GuardAutenticacion>
  );
}