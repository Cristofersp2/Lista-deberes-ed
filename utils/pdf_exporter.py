# utils/pdf_exporter.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from datetime import datetime

# Detectar disponibilidad de reportlab
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    from models.tarea import Tarea
except ImportError:
    # Fallback para testing directo (no recomendado en producción)
    class Tarea:
        def __init__(self, titulo="", descripcion="", fecha_limite="", completada=False):
            self.titulo = titulo
            self.descripcion = descripcion
            self.fecha_limite = fecha_limite
            self.completada = completada


class PDFExporter:
    @staticmethod
    def exportar(tareas: List[Tarea], ruta_salida: str):
        if not REPORTLAB_AVAILABLE:
            raise RuntimeError("reportlab no está instalado. Ejecuta: pip install reportlab")

        doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(A4))
        elementos = []

        styles = getSampleStyleSheet()
        titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], fontSize=20, spaceAfter=14,
                               textColor=colors.HexColor("#1976D2"), alignment=1)
        subtitulo = ParagraphStyle('Sub', fontSize=11, textColor=colors.grey, alignment=1)

        elementos.append(Paragraph("📋 LISTA DE DEBERES — ESTRUCTURA DE DATOS", titulo))
        elementos.append(Paragraph(f"📅 {datetime.now():%d de %B de %Y, %H:%M}", subtitulo))
        elementos.append(Spacer(1, 20))

        datos = [["✔️", "TÍTULO", "DESCRIPCIÓN", "FECHA"]]
        for t in tareas:
            estado = "✅" if t.completada else "⏳"
            desc = (t.descripcion[:50] + "..." if len(t.descripcion) > 50 else t.descripcion) or "—"
            datos.append([estado, t.titulo, desc, t.fecha_limite or "—"])

        tabla = Table(datos, colWidths=[0.6*inch, 2*inch, 3.5*inch, 1*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1976D2")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ]))
        elementos.append(tabla)

        elementos.append(Spacer(1, 20))
        completadas = sum(t.completada for t in tareas)
        elementos.append(Paragraph(f"📊 Total: {len(tareas)} | ✅ {completadas} | ⏳ {len(tareas)-completadas}", styles["Normal"]))

        doc.build(elementos)