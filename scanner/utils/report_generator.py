from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors
from openpyxl import Workbook


# 🔥 PDF GENERATOR
def generate_pdf(file_path, data):
    doc = SimpleDocTemplate(file_path)

    table_data = [["SSID", "Encryption", "RSSI", "Classification", "Score"]]

    for d in data:
        table_data.append([
            d.ssid,
            d.encryption,
            d.rssi,
            d.classification,
            d.trust_score
        ])

    table = Table(table_data)
    table.setStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white)
    ])

    doc.build([table])


# 🔥 EXCEL GENERATOR
def generate_excel(file_path, data):
    wb = Workbook()
    ws = wb.active

    ws.append(["SSID", "Encryption", "RSSI", "Classification", "Score"])

    for d in data:
        ws.append([
            d.ssid,
            d.encryption,
            d.rssi,
            d.classification,
            d.trust_score
        ])

    wb.save(file_path)