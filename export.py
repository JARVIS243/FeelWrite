# export.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# --- Export as TXT ---
def export_to_txt(filename, content):
    folder = os.path.dirname(filename)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

# --- Export as PDF ---
def export_to_pdf(filename, content):
    folder = os.path.dirname(filename)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    x, y = 40, height - 50

    for line in content.split("\n"):
        if y <= 40:
            c.showPage()
            y = height - 50
        c.drawString(x, y, line)
        y -= 15

    c.save()
    return filename
