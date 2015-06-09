import os
import unittest
from datetime import datetime, date

from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item, Transaction
from pyinvoice.templates import SimpleInvoice


class TestSimpleInvoice(unittest.TestCase):
    def setUp(self):
        self.file_base_dir = os.path.dirname(os.path.realpath(__file__))

    def test_simple(self):
        invoice_path = os.path.join(self.file_base_dir, 'fixtures/dist/simple.pdf')
        doc = SimpleInvoice(invoice_path)

        doc.is_paid = True

        doc.invoice_info = InvoiceInfo('1024', datetime.now(), datetime.now())

        doc.service_provider_info = ServiceProviderInfo(
            name='PyInvoice',
            street='My Street',
            city='My City',
            state='My State',
            country='My Country',
            post_code='222222',
            vat_tax_number='Vat/Tax number'
        )

        doc.client_info = ClientInfo(
            email='My Email',
            client_id='My Client Id',
            name='Client Name',
            street='Client Street',
            city='Client City',
            state='Client State',
            country='Client country',
            post_code='222222'
        )

        doc.add_item(Item('Item', 'Item desc', 1, '1.1'))
        doc.add_item(Item('Item', 'Item desc', 2, '2.2'))
        doc.add_item(Item('Item', 'Item desc', 3, '3.3'))

        items = doc.items
        self.assertEqual(len(items), 3)

        doc.set_item_tax_rate(20)  # 20%

        doc.add_transaction(Transaction('Paypal', 111, datetime.now(), 1))
        doc.add_transaction(Transaction('Strip', 222, date.today(), 2))

        transactions = doc.transactions
        self.assertEqual(len(transactions), 2)

        doc.set_bottom_tip("Email: example@example.com<br />Don't hesitate to contact us for any questions.")

        doc.finish()

        self.assertTrue(os.path.exists(invoice_path))