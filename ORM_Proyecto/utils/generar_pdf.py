import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

def generar_pdf_boleta(cliente, carrito):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    carpeta_boletas = os.path.join(base_dir, "boletas")
    os.makedirs(carpeta_boletas, exist_ok=True)

    fecha_creacion = datetime.now()
    archivo_pdf = os.path.join(
        carpeta_boletas,
        f"boleta_{cliente.nombre}_{fecha_creacion.strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    )

    c = canvas.Canvas(archivo_pdf, pagesize=letter)
    width, height = letter

    margen_x = 50
    margen_y = height - 50
    linea_separacion = 20

    c.setFillColor(colors.lightgrey)
    c.rect(0, height - 80, width, 80, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Times-Italic", 18)
    c.drawString(margen_x, height - 40, "Universidad Católica de Temuco")
    c.setFont("Times-Italic", 12)
    c.drawString(margen_x, height - 60, "Boleta de Pedido")

    numero_boleta = f"{fecha_creacion.strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
    margen_y -= 70
    c.setFont("Times-Italic", 12)
    c.drawString(margen_x, margen_y, f"Número de Boleta: {numero_boleta}")

    margen_y -= 15
    c.setLineWidth(0.5)
    c.setStrokeColor(colors.grey)
    c.line(margen_x, margen_y, width - margen_x, margen_y)

    margen_y -= 30
    c.setFont("Times-Italic", 12)
    c.drawString(margen_x, margen_y, "Información del Cliente:")
    c.setFont("Times-Italic", 11)
    c.drawString(margen_x, margen_y - linea_separacion, f"Nombre: {cliente.nombre}")
    c.drawString(margen_x, margen_y - 2 * linea_separacion, f"Email: {cliente.email}")

    margen_y -= 80
    c.setFont("Times-Italic", 12)
    c.drawString(margen_x, margen_y, "Detalles del Pedido:")

    datos_pedido = [["Menú", "Cantidad", "Precio Unitario (CLP)", "Total (CLP)"]]
    for item in carrito:
        menu = item["menu"]
        cantidad = item["cantidad"]
        total = item["total"]
        datos_pedido.append([menu.nombre, cantidad, f"{menu.precio:.2f}", f"{total:.2f}"])

    tabla = Table(datos_pedido, colWidths=[150, 100, 150, 100])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Italic'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    tabla.wrapOn(c, margen_x, margen_y - 50)
    tabla.drawOn(c, margen_x, margen_y - 100)

    total_general = sum(item["total"] for item in carrito)
    margen_y -= 180
    c.setFont("Times-Italic", 12)
    c.drawString(margen_x, margen_y, f"Total General: {total_general:.2f} CLP")
    c.setFont("Times-Italic", 11)
    c.drawString(margen_x, margen_y - linea_separacion, f"Fecha de creación: {fecha_creacion.strftime('%Y-%m-%d')}")
    c.drawString(margen_x, margen_y - 2 * linea_separacion, f"Hora de creación: {fecha_creacion.strftime('%H:%M:%S')}")

    c.setFont("Times-Italic", 10)
    c.setFillColor(colors.darkgrey)
    c.drawString(margen_x, 30, "Gracias por su preferencia. Si tiene dudas, contáctenos.")

    c.save()
    return archivo_pdf
