from reportlab.platypus import Paragraph, Table
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors


class CodeSnippet(Paragraph):
    style = ParagraphStyle(
        name='CodeSnippet',
        parent=getSampleStyleSheet()['Code'],
        backColor=colors.lightgrey, leftIndent=0,
        borderPadding=(5, 5, 5, 5)
    )

    def __init__(self, code):
        Paragraph.__init__(self, code, self.style)


class AddressTable(Table):
    def __init__(self, data, horizontal_align=None):
        Table.__init__(self, data, hAlign=horizontal_align)