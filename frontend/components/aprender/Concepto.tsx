interface PropiedadesConcepto {
  titulo: string;
  children: React.ReactNode;
}

export function Concepto({ titulo, children }: PropiedadesConcepto) {
  return (
    <section className="flex flex-col gap-3 border-b border-white/10 pb-8">
      <h2 className="text-xl font-semibold text-claridata-texto">{titulo}</h2>
      <div className="text-base leading-relaxed text-claridata-textoSecundario">
        {children}
      </div>
    </section>
  );
}