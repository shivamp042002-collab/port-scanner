from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors

def generate_pdf(file_path, scan_data):

    doc = SimpleDocTemplate(file_path)

    table_data = [["Port", "Service", "Status"]]

    for item in scan_data:
        table_data.append([item.port, item.service, item.status])

    table = Table(table_data)
    table.setStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('GRID',(0,0),(-1,-1),1,colors.green)
    ])

    doc.build([table])