from infraestructura.base_de_datos.modelos.informe_modelo import InformeModelo
from infraestructura.base_de_datos.repositorios.repositorio_informe import RepositorioInforme


class ListarInformesGuardados:
    def __init__(self, repositorio_informe: RepositorioInforme) -> None:
        self._repositorio_informe = repositorio_informe

    def ejecutar(self, usuario_id: str) -> list[InformeModelo]:
        return self._repositorio_informe.obtener_guardados_por_usuario(usuario_id)