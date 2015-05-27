from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate


class SimpleInvoice(SimpleDocTemplate):
    def __init__(self, invoice_path):
        SimpleDocTemplate.__init__(
            self,
            invoice_path,
            pagesize=letter,
            rightMargin=.25 * inch,
            leftMargin=.25 * inch,
            topMargin=.25 * inch,
            bottomMargin=.25 * inch
        )