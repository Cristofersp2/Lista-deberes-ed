import json
import os
from typing import List
from models.tarea import Tarea

class TareaRepository:
    """
    Capa de persistencia: gestiona el almacenamiento en JSON.
    ✅ Abstrae el acceso a datos
    ✅ Usa composición (lista de Tarea)
    ✅ Single Responsibility Principle
    """
    def __init__(self, archivo_json: str = "tareas.json"):
        self.archivo_json = archivo_json
        self._tareas: List[Tarea] = []
        self.cargar_desde_json()

    @property
    def tareas(self) -> List[Tarea]:
        return self._tareas.copy()  # Evita modificación externa directa

    def agregar(self, tarea: Tarea):
        self._tareas.append(tarea)
        self.guardar_en_json()

    def eliminar_por_indice(self, indice: int):
        if 0 <= indice < len(self._tareas):
            self._tareas.pop(indice)
            self.guardar_en_json()
        else:
            raise IndexError("Índice fuera de rango.")

    def actualizar_por_indice(self, indice: int, tarea: Tarea):
        if 0 <= indice < len(self._tareas):
            self._tareas[indice] = tarea
            self.guardar_en_json()
        else:
            raise IndexError("Índice fuera de rango.")

    def marcar_completada(self, indice: int, valor: bool = True):
        if 0 <= indice < len(self._tareas):
            self._tareas[indice].completada = valor
            self.guardar_en_json()
        else:
            raise IndexError("Índice fuera de rango.")

    def ordenar_por_fecha(self, ascendente: bool = True):
        """Ordena por fecha límite (más próximas primero si ascendente=True)."""
        def clave(t: Tarea):
            if not t.fecha_limite:
                return float('inf') if ascendente else float('-inf')
            try:
                return int(t.fecha_limite.replace("-", ""))
            except:
                return float('inf') if ascendente else float('-inf')
        self._tareas.sort(key=clave, reverse=not ascendente)
        self.guardar_en_json()

    def cargar_desde_json(self):
        """Carga tareas desde JSON y las convierte en instancias de Tarea."""
        self._tareas = []
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    for item in datos:
                        try:
                            tarea = Tarea.from_dict(item)
                            self._tareas.append(tarea)
                        except ValueError as e:
                            print(f"[⚠️] Tarea ignorada (JSON inválido): {e}")
            except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
                print(f"[❌] Error al cargar {self.archivo_json}: {e}")

    def guardar_en_json(self):
        """Guarda la lista de tareas en JSON."""
        try:
            datos = [t.to_dict() for t in self._tareas]
            with open(self.archivo_json, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[❌] Error al guardar en {self.archivo_json}: {e}")