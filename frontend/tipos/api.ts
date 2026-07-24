export interface TokenRespuesta {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface DatasetRespuesta {
  id: string;
  usuario_id: string;
  nombre_archivo: string;
  tipo_archivo: string;
  tamaño_archivo: number;
  numero_filas: number | null;
  numero_columnas: number | null;
  columnas: string[] | null;
  tipos_datos: Record<string, string> | null;
  fecha_creacion: string;
  fecha_actualizacion: string;
}

export interface EstadisticasColumnaNumerica {
  columna: string;
  media: number;
  mediana: number;
  desviacion_estandar: number;
  minimo: number;
  maximo: number;
}

export interface EstadisticasDescriptivas {
  metadatos: {
    numero_filas: number;
    numero_columnas: number;
    nombres_columnas: string[];
    tipos_datos: Record<string, string>;
  };
  valores_nulos: {
    por_columna: Record<string, number>;
    total: number;
  };
  clasificacion_variables: {
    numericas: string[];
    categoricas: string[];
  };
  columnas: EstadisticasColumnaNumerica[];
}
export type SeveridadDescubrimiento =
  | "INFORMATIVO"
  | "ATENCION"
  | "IMPORTANTE"
  | "CRITICO";

export interface DescubrimientoRespuesta {
  tipo: string;
  titulo: string;
  descripcion: string;
  severidad: SeveridadDescubrimiento;
  columna: string | null;
  valor: number | null;
  recomendacion: string | null;
}
export interface InformeDetalleRespuesta {
  id: string;
  usuario_id: string;
  dataset_id: string;
  titulo: string;
  guardado: boolean;
  resumen_ejecutivo: string | null;
  estadisticas_descriptivas: EstadisticasDescriptivas | null;
  analisis_distribucion: Record<string, unknown> | null;
  correlaciones: Record<string, unknown> | null;
  deteccion_outliers: Record<string, unknown> | null;
  hallazgos_principales: Record<string, unknown> | null;
  recomendaciones: Record<string, unknown> | null;
  conclusiones: string | null;
  descubrimientos: DescubrimientoRespuesta[] | null;
  fecha_creacion: string;
  fecha_actualizacion: string;
  interpretacion_profesional: SeccionInterpretacionRespuesta[] | null;
  recomendaciones_inteligentes: RecomendacionRespuesta[] | null;
  visualizaciones_inteligentes: VisualizacionRespuesta[] | null;
}

export interface InformeResumenRespuesta {
  id: string;
  titulo: string;
  dataset_id: string;
  fecha_creacion: string;
  fecha_actualizacion: string;
}

export interface ErrorApi {
  detalle: string;
}

export interface SeccionInterpretacionRespuesta {
  tipo: string;
  titulo: string;
  parrafos: string[];
}

export type PrioridadRecomendacion = "ALTA" | "MEDIA" | "BAJA";

export interface RecomendacionRespuesta {
  titulo: string;
  categoria: string;
  prioridad: PrioridadRecomendacion;
  razon: string;
  accion: string;
}


export type TipoVisualizacion =
  | "HISTOGRAMA"
  | "BOXPLOT"
  | "SCATTER"
  | "HEATMAP"
  | "BARRAS"
  | "DISTRIBUCION";

export type PrioridadVisualizacion = "ALTA" | "MEDIA" | "BAJA";

export interface VisualizacionRespuesta {
  tipo: TipoVisualizacion;
  titulo: string;
  descripcion: string;
  prioridad: PrioridadVisualizacion;
  motivo: string;
  variables: string[];
  configuracion: Record<string, unknown>;
}