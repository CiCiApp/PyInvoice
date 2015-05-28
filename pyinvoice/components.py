from reportlab.platypus import Paragraph, Table, TableStyle, Flowable
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


class SimpleTable(Table):
    style = TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), .25, colors.black),
        ('BOX', (0, 0), (-1, -1), .25, colors.black),
    ])

    def __init__(self, data, horizontal_align=None):
        Table.__init__(self, data, style=self.style, hAlign=horizontal_align)


class PaidStamp(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self, canvas, doc):
        # TODO: xxx
        canvas.saveState()
        canvas.drawString(self.x, self.y, 'PAID')
        canvas.restoreState()