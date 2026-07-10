export interface PuntoDato {
  id: string;
  valor: number;
}

export interface ResultadosEstadisticos {
  media: number;
  mediana: number;
  moda: number[];
}

export interface ConfiguracionLaboratorio {
  valorMinimo: number;
  valorMaximo: number;
  etiquetaUnidad: string;
  titulo: string;
  descripcionContexto: string;
}

export type AccionLaboratorio =
  | { tipo: "MOVER_PUNTO"; id: string; nuevoValor: number }
  | { tipo: "AGREGAR_PUNTO" }
  | { tipo: "ELIMINAR_PUNTO"; id: string }
  | { tipo: "EDITAR_VALOR"; id: string; nuevoValor: number };

export interface EstadoLaboratorio {
  puntos: PuntoDato[];
}