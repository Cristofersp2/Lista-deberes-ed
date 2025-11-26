# main.py
import tkinter as tk
from views.app_view import AppView
from data.tarea_repository import TareaRepository
from models.tarea import Tarea
import sys
import subprocess
import importlib


class Controlador:
    def __init__(self):
        self.repo = TareaRepository()
        self.root = tk.Tk()
        self.vista = AppView(self.root)

        # Conectar callbacks
        self.vista.set_on_agregar(self.agregar_tarea)
        self.vista.set_on_ordenar(self.ordenar_por_fecha)
        self.vista.set_on_exportar_pdf(self.exportar_a_pdf)
        self.vista.set_on_marcar(self.marcar_completada)
        self.vista.set_on_eliminar(self.eliminar_tarea)

        # Inicializar vista
        self.vista.actualizar_lista(self.repo.tareas)

    def agregar_tarea(self, titulo: str, descripcion: str, fecha: str):
        try:
            if not titulo.strip():
                raise ValueError("El título no puede estar vacío.")
            
            # Validar fecha
            if fecha:
                from datetime import datetime
                datetime.strptime(fecha, "%Y-%m-%d")  # Solo valida, no usa

            tarea = Tarea(titulo=titulo, descripcion=descripcion, fecha_limite=fecha)
            self.repo.agregar(tarea)
            self.vista.actualizar_lista(self.repo.tareas)
            self.vista.limpiar_campos()
            self.vista.mostrar_info("✅ Éxito", f"Tarea '{tarea.titulo}' añadida.")

        except ValueError as e:
            self.vista.mostrar_error(f"⚠️ Entrada inválida:\n{e}")
        except Exception as e:
            self.vista.mostrar_error(f"❌ Error inesperado:\n{e}")

    def ordenar_por_fecha(self, ascendente: bool):
        try:
            self.repo.ordenar_por_fecha(ascendente=ascendente)
            self.vista.actualizar_lista(self.repo.tareas)
            orden = "más próximas primero" if ascendente else "más lejanas primero"
            self.vista.mostrar_info("✅ Ordenado", f"Tareas ordenadas: {orden}.")
        except Exception as e:
            self.vista.mostrar_error(f"❌ Error al ordenar:\n{e}")

    def exportar_a_pdf(self):
        try:
            from utils.pdf_exporter import PDFExporter, REPORTLAB_AVAILABLE
        except ImportError:
            REPORTLAB_AVAILABLE = False

        if not REPORTLAB_AVAILABLE:
            instalar = self.vista.root.tk.call("tk", "messageBox",
                                               "-type", "yesno",
                                               "-icon", "question",
                                               "-message", "¿Instalar 'reportlab' para exportar a PDF?",
                                               "-title", "📦 Módulo faltante")
            if instalar == "yes":
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
                    # Recargar módulo
                    import utils.pdf_exporter
                    importlib.reload(utils.pdf_exporter)
                    from utils.pdf_exporter import PDFExporter, REPORTLAB_AVAILABLE
                    self.vista.mostrar_info("✅ Éxito", "reportlab instalado. Vuelva a exportar.")
                except Exception as e:
                    self.vista.mostrar_error(f"❌ Error al instalar:\n{e}")
            return

        if not self.repo.tareas:
            self.vista.mostrar_info("ℹ️ Sin datos", "No hay tareas para exportar.")
            return

        # Exportar solo tareas pendientes (no completadas)
        tareas_pendientes = [t for t in self.repo.tareas if not t.completada]
        if not tareas_pendientes:
            self.vista.mostrar_info("ℹ️ Sin pendientes", "No hay tareas pendientes para exportar.")
            return

        ruta = self.vista.root.tk.call("tk", "getSaveFile",
                                       "-defaultextension", ".pdf",
                                       "-filetypes", "{{PDF files} {.pdf}}",
                                       "-initialfile", "Informe_Tareas_EDD.pdf")
        if not ruta:
            return

        try:
            # Asegurar que la carpeta destino exista
            import os
            carpeta = os.path.dirname(ruta)
            if carpeta and not os.path.exists(carpeta):
                os.makedirs(carpeta, exist_ok=True)

            PDFExporter.exportar(tareas_pendientes, ruta)
            self.vista.mostrar_info("✅ PDF generado", f"Guardado en:\n{ruta}")
        except Exception as e:
            self.vista.mostrar_error(f"❌ Error al generar PDF:\n{e}")

    def marcar_completada(self, indice: int):
        try:
            if not (0 <= indice < len(self.repo.tareas)):
                raise IndexError("Índice fuera de rango.")
            nuevo_estado = not self.repo.tareas[indice].completada
            self.repo.marcar_completada(indice, nuevo_estado)
            self.vista.actualizar_lista(self.repo.tareas)
        except Exception as e:
            self.vista.mostrar_error(f"❌ Error al marcar:\n{e}")

    def eliminar_tarea(self, indice: int):
        try:
            if not (0 <= indice < len(self.repo.tareas)):
                raise IndexError("Índice fuera de rango.")
            
            tarea = self.repo.tareas[indice]
            confirm = self.vista.root.tk.call("tk", "messageBox",
                                             "-type", "yesno",
                                             "-icon", "warning",
                                             "-message", f"¿Eliminar tarea '{tarea.titulo}'?",
                                             "-title", "🗑️ Confirmar eliminación")
            if confirm == "yes":
                self.repo.eliminar_por_indice(indice)
                self.vista.actualizar_lista(self.repo.tareas)
                self.vista.mostrar_info("✅ Eliminada", f"Tarea '{tarea.titulo}' eliminada.")
        except Exception as e:
            self.vista.mostrar_error(f"❌ Error al eliminar:\n{e}")

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Controlador()
    app.ejecutar()