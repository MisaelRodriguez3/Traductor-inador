from docx.document import Document
from docx.shared import Pt, RGBColor
from app.utils.error_handler import handle_error

def add_watermark(doc: Document, text: str):
    try: 

        section = doc.sections[0]
        footer = section.footer

        paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        paragraph.alignment = 0

        run = paragraph.add_run(text)
        run.font.name = 'Century Gothic'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(239, 210, 132)  
        run.bold = True

        run._element.get_or_add_rPr()
    except Exception as e:
        handle_error(e)
