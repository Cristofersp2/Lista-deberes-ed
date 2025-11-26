# views/app_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Callable, Optional
from data.tarea_repository import TareaRepository


class AppView:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎓 Lista de Deberes — Estructura de Datos")
        self.root.geometry("850x600")
        self.root.minsize(800, 550)

        # Componentes UI
        self.entry_titulo: Optional[tk.Entry] = None
        self.entry_desc: Optional[tk.Entry] = None
        self.entry_fecha: Optional[tk.Entry] = None
        self.tree: Optional[ttk.Treeview] = None

        self._crear_widgets()

    def _crear_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), 
                        background="#1976D2", foreground="white")

        # === Frame: Nueva Tarea ===
        frame_input = tk.LabelFrame(self.root, text="➕ Nueva Tarea", 
                                   padx=10, pady=10, font=("Segoe UI", 10, "bold"))
        frame_input.pack(fill="x", padx=15, pady=(10, 5))

        tk.Label(frame_input, text="Título:", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_titulo = tk.Entry(frame_input, width=30, font=("Segoe UI", 10))
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Descripción:", font=("Segoe UI", 9)).grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.entry_desc = tk.Entry(frame_input, width=35, font=("Segoe UI", 10))
        self.entry_desc.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_input, text="Fecha (AAAA-MM-DD):", font=("Segoe UI", 9)).grid(row=0, column=4, sticky="e", padx=5, pady=5)
        self.entry_fecha = tk.Entry(frame_input, width=12, font=("Segoe UI", 10))
        self.entry_fecha.grid(row=0, column=5, padx=5, pady=5)
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))

        btn_agregar = tk.Button(frame_input, text="➕ Añadir", command=self._on_agregar,
                                bg="#2196F3", fg="white", font=("Segoe UI", 9))
        btn_agregar.grid(row=0, column=6, padx=10)

        # === Frame: Botones superiores ===
        frame_botones = tk.Frame(self.root, padx=15, pady=5)
        frame_botones.pack(fill="x")

        tk.Button(frame_botones, text="↑ Ordenar (próximas)", command=self._on_ordenar_asc,
                  bg="#FF9800", fg="white", font=("Segoe UI", 9)).pack(side="left", padx=5)
        tk.Button(frame_botones, text="↓ Ordenar (lejanas)", command=self._on_ordenar_desc,
                  bg="#FF9800", fg="white", font=("Segoe UI", 9)).pack(side="left", padx=5)
        tk.Button(frame_botones, text="📦 Exportar pendientes (PDF)", command=self._on_exportar_pdf,
              bg="#9C27B0", fg="white", font=("Segoe UI", 9)).pack(side="right", padx=5)

        # === Tabla de tareas ===
        frame_tree = tk.Frame(self.root, padx=15, pady=5)
        frame_tree.pack(fill="both", expand=True)

        columns = ("Estado", "Título", "Descripción", "Fecha")
        self.tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=15)
        self.tree.pack(side="left", fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            width = 130 if col == "Descripción" else 90
            self.tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # === Botones inferiores ===
        frame_acciones = tk.Frame(self.root, padx=15, pady=5)
        frame_acciones.pack(fill="x")

        tk.Button(frame_acciones, text="✔️ Marcar/Desmarcar", command=self._on_marcar,
                  font=("Segoe UI", 9)).pack(side="left", padx=5)
        tk.Button(frame_acciones, text="🗑️ Eliminar", command=self._on_eliminar,
                  bg="#f44336", fg="white", font=("Segoe UI", 9)).pack(side="left", padx=5)

    # --- Métodos de eventos ---
    def set_on_agregar(self, callback: Callable[[str, str, str], None]):
        self._on_agregar_cb = callback

    def set_on_ordenar(self, callback: Callable[[bool], None]):
        self._on_ordenar_cb = callback

    def set_on_exportar_pdf(self, callback: Callable[[], None]):
        self._on_exportar_pdf_cb = callback

    def set_on_marcar(self, callback: Callable[[int], None]):
        self._on_marcar_cb = callback

    def set_on_eliminar(self, callback: Callable[[int], None]):
        self._on_eliminar_cb = callback

    def _on_agregar(self):
        if hasattr(self, '_on_agregar_cb'):
            titulo = self.entry_titulo.get().strip()
            desc = self.entry_desc.get().strip()
            fecha = self.entry_fecha.get().strip()
            self._on_agregar_cb(titulo, desc, fecha)

    def _on_ordenar_asc(self):
        if hasattr(self, '_on_ordenar_cb'):
            self._on_ordenar_cb(True)

    def _on_ordenar_desc(self):
        if hasattr(self, '_on_ordenar_cb'):
            self._on_ordenar_cb(False)

    def _on_exportar_pdf(self):
        if hasattr(self, '_on_exportar_pdf_cb'):
            self._on_exportar_pdf_cb()

    def _on_marcar(self):
        if hasattr(self, '_on_marcar_cb'):
            sel = self.tree.selection()
            if sel:
                try:
                    idx = int(sel[0])  # ✅ Usa el índice real (iid = str(índice))
                    self._on_marcar_cb(idx)
                except (ValueError, IndexError):
                    self.mostrar_error("Índice inválido.")
            else:
                messagebox.showinfo("ℹ️", "Seleccione una tarea.")

    def _on_eliminar(self):
        if hasattr(self, '_on_eliminar_cb'):
            sel = self.tree.selection()
            if sel:
                try:
                    idx = int(sel[0])  # ✅ Índice real
                    self._on_eliminar_cb(idx)
                except (ValueError, IndexError):
                    self.mostrar_error("Índice inválido.")
            else:
                messagebox.showinfo("ℹ️", "Seleccione una tarea.")

    # --- Métodos públicos ---
    def actualizar_lista(self, tareas: list):
        """Actualiza la tabla con iid = índice real"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, t in enumerate(tareas):
            estado = "✅" if t.completada else "⏳"
            desc = (t.descripcion[:50] + "..." if len(t.descripcion) > 50 else t.descripcion) or "—"
            # ✅ iid = índice real como string
            self.tree.insert("", "end", iid=str(i), values=(
                estado, t.titulo, desc, t.fecha_limite or "—"
            ))

    def limpiar_campos(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_titulo.focus()

    def mostrar_error(self, mensaje: str):
        messagebox.showerror("❌ Error", mensaje)

    def mostrar_info(self, titulo: str, mensaje: str):
        messagebox.showinfo(titulo, mensaje)