export type EstadoAnalisis = "idle" | "selected" | "loading" | "result";

export interface ArchivoSeleccionado {
  nombre: string;
  tamañoBytes: number;
  extension: string;
}