from __future__ import unicode_literals
from datetime import datetime, date
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph
from pyinvoice.components import SimpleTable, TableWithHeader, PaidStamp
from pyinvoice.models import PDFInfo, Item, Transaction, InvoiceInfo, ServiceProviderInfo, ClientInfo


class SimpleInvoice(SimpleDocTemplate):
    default_pdf_info = PDFInfo(title='Invoice', author='CiCiApp.com', subject='Invoice')

    def __init__(self, invoice_path, pdf_info=None):
        if not pdf_info:
            pdf_info = self.default_pdf_info

        SimpleDocTemplate.__init__(
            self,
            invoice_path,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch,
            **pdf_info.__dict__
        )

        self.invoice_info = None
        self.service_provider_info = None
        self.client_info = None
        self.is_paid = False
        self._items = []
        self._transactions = []

    @property
    def items(self):
        return self._items[:]

    def add_item(self, item):
        if isinstance(item, Item):
            self._items.append(item)

    @property
    def transactions(self):
        return self._transactions[:]

    def add_transaction(self, t):
        if isinstance(t, Transaction):
            self._transactions.append(t)

    @staticmethod
    def __attribute_to_table_data(instance, attribute_verbose_name_list):
        data = []

        for p, v in attribute_verbose_name_list:
            attr = getattr(instance, p)
            if attr is not None:
                if isinstance(attr, datetime):
                    attr = attr.strftime('%Y-%m-%d %H:%M')
                elif isinstance(attr, date):
                    attr = attr.strftime('%Y-%m-%d')
                data.append(['{0}:'.format(v), attr])

        return data

    def finish(self):
        story = []

        if isinstance(self.invoice_info, InvoiceInfo):
            props = [('invoice_id', 'Invoice id'), ('invoice_datetime', 'Invoice date'),
                     ('due_datetime', 'Invoice due date')]

            story.append(
                SimpleTable(self.__attribute_to_table_data(self.invoice_info, props), horizontal_align='LEFT')
            )

        if isinstance(self.service_provider_info, ServiceProviderInfo):
            props = [('name', 'Name'), ('street', 'Street'), ('city', 'City'), ('state', 'State'),
                     ('country', 'Country'), ('post_code', 'Post code')]

            story.append(
                SimpleTable(self.__attribute_to_table_data(self.service_provider_info, props), horizontal_align='RIGHT')
            )

        if isinstance(self.client_info, ClientInfo):
            props = [('name', 'Name'), ('street', 'Street'), ('city', 'City'), ('state', 'State'),
                     ('country', 'Country'), ('post_code', 'Post code'), ('email', 'Email'), ('client_id', 'Client id')]
            story.append(SimpleTable(self.__attribute_to_table_data(self.client_info, props), horizontal_align='LEFT'))

        item_table_paragraph_style = ParagraphStyle(
            'ItemTableParagraph',
            parent=getSampleStyleSheet()['Normal'],
            alignment=TA_CENTER
        )

        item_data = [(
            item.item_id,
            item.name,
            Paragraph(item.description, item_table_paragraph_style),
            item.units,
            item.unit_price,
            item.subtotal
        ) for item in self._items if isinstance(item, Item)]
        if item_data:
            item_data.insert(0, ('Item id', 'Name', 'Description', 'Units', 'Unit Price', 'Subtotal'))
            story.append(TableWithHeader(item_data, horizontal_align='LEFT'))

        self.build(story, onFirstPage=PaidStamp(7*inch, 5.8*inch) if self.is_paid else None)