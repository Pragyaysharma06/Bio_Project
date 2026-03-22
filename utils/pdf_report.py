from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data):
    doc = SimpleDocTemplate("/tmp/report.pdf")
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"Disease: {data['disease']}", styles['Normal']))
    content.append(Paragraph(f"Gene: {data['gene']}", styles['Normal']))

    content.append(Paragraph("Proteins:", styles['Heading2']))
    for p in data['proteins']:
        content.append(Paragraph(p, styles['Normal']))

    content.append(Paragraph("Drugs:", styles['Heading2']))
    for d in data['drugs']:
        content.append(Paragraph(d, styles['Normal']))

    doc.build(content)