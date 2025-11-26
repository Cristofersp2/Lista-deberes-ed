from datetime import datetime

class Tarea:
    """
    Modelo de datos: representa una tarea.
    ✅ Encapsulación
    ✅ Validación de datos en el constructor
    ✅ Métodos de serialización
    """
    def __init__(self, titulo: str, descripcion: str = "", fecha_limite: str = "", completada: bool = False):
        self.titulo = self._validar_titulo(titulo)
        self.descripcion = descripcion.strip()
        self.fecha_limite = self._validar_fecha(fecha_limite)
        self.completada = bool(completada)

    @staticmethod
    def _validar_titulo(titulo: str) -> str:
        titulo = titulo.strip()
        if not titulo:
            raise ValueError("El título no puede estar vacío.")
        if len(titulo) > 100:
            raise ValueError("El título no puede exceder 100 caracteres.")
        return titulo

    @staticmethod
    def _validar_fecha(fecha_str: str) -> str:
        if not fecha_str:
            return ""
        fecha_str = fecha_str.strip()
        try:
            # Normaliza a YYYY-MM-DD
            dt = datetime.strptime(fecha_str, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use AAAA-MM-DD.")

    def to_dict(self) -> dict:
        """Serializa la tarea a diccionario (para JSON)."""
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "fecha_limite": self.fecha_limite,
            "completada": self.completada
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Deserializa un diccionario a una instancia de Tarea."""
        try:
            return cls(
                titulo=data["titulo"],
                descripcion=data.get("descripcion", ""),
                fecha_limite=data.get("fecha_limite", ""),
                completada=data.get("completada", False)
            )
        except (KeyError, ValueError) as e:
            raise ValueError(f"Datos inválidos para crear Tarea: {e}")

    def __repr__(self):
        return f"<Tarea '{self.titulo}' | {self.fecha_limite} | {'✅' if self.completada else '⏳'}>"