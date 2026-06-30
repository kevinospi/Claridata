export type Dificultad = "Principiante" | "Intermedio" | "Avanzado";

export interface EjercicioRespuestaNumerica {
  id: string;
  pregunta: string;
  datos: number[];
  respuestaCorrecta: number;
  explicacion: string;
}

export interface ContenidoTema {
  queEs: string;
  paraQueSirve: string;
  cuandoUsarla: string;
  cuandoNoUsarla: string;
  ejemplo: string;
  erroresComunes: string[];
  conceptosRelacionados: string[];
}

export interface Tema {
  id: string;
  nombre: string;
  descripcion: string;
  dificultad: Dificultad;
  tiempoLectura: string;
  contenido: ContenidoTema;
  ejercicios: EjercicioRespuestaNumerica[];
}