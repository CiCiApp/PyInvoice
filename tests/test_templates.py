from decimal import Decimal
import os
import unittest
from datetime import datetime, date

from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item, Transaction
from pyinvoice.templates import SimpleInvoice


class TestSimpleInvoice(unittest.TestCase):
    def setUp(self):
        self.file_base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures/dist')

    def test_simple(self):
        invoice_path = os.path.join(self.file_base_dir, 'simple.pdf')

        if os.path.exists(invoice_path):
            os.remove(invoice_path)

        doc = SimpleInvoice(invoice_path)

        doc.is_paid = True

        doc.invoice_info = InvoiceInfo(1023, datetime.now(), datetime.now())

        doc.service_provider_info = ServiceProviderInfo(
            name='PyInvoice',
            street='My Street',
            city='My City',
            state='My State',
            country='My Country',
            post_code='222222',
            vat_tax_number='Vat/Tax number'
        )

        doc.client_info = ClientInfo(email='client@example.com')

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

    def test_only_items(self):
        invoice_path = os.path.join(self.file_base_dir, 'only_items.pdf')
        if os.path.exists(invoice_path):
            os.remove(invoice_path)

        invoice = SimpleInvoice(invoice_path)

        # Before add items
        item_data, item_subtotal = invoice._item_raw_data_and_subtotal()
        self.assertEqual(len(item_data), 0)
        self.assertEqual(item_subtotal, Decimal('0'))
        item_data, style = invoice._item_data_and_style()
        self.assertEqual(len(item_data), 0)
        self.assertEqual(style, [])

        # Add items
        invoice.add_item(Item('Item1', 'Item desc', 1, 1.1))
        invoice.add_item(Item('Item2', 'Item desc', 2, u'2.2'))
        invoice.add_item(Item(u'Item3', 'Item desc', 3, '3.3'))

        # After add items
        items = invoice.items
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].name, 'Item1')
        self.assertEqual(items[0].amount, Decimal('1.1'))
        self.assertEqual(items[1].amount, Decimal('4.4'))
        self.assertEqual(items[2].name, u'Item3')
        self.assertEqual(items[2].amount, Decimal('9.9'))

        item_data, item_subtotal = invoice._item_raw_data_and_subtotal()
        self.assertEqual(item_subtotal, Decimal('15.4'))
        self.assertEqual(len(item_data), 3)

        item_data, style = invoice._item_data_and_style()
        self.assertEqual(len(item_data), 6)  # header, subtotal, total
        self.assertEqual(item_data[-2][-1], Decimal('15.4'))  # subtotal
        self.assertEqual(item_data[-1][-1], Decimal('15.4'))  # total

        invoice.finish()

        self.assertTrue(os.path.exists(invoice_path))

    def test_only_items_with_tax_rate(self):
        invoice_path = os.path.join(self.file_base_dir, 'only_items.pdf')
        if os.path.exists(invoice_path):
            os.remove(invoice_path)

        invoice = SimpleInvoice(invoice_path)

        # Before add items
        item_data, item_subtotal = invoice._item_raw_data_and_subtotal()
        self.assertEqual(len(item_data), 0)
        self.assertEqual(item_subtotal, Decimal('0'))
        item_data, style = invoice._item_data_and_style()
        self.assertEqual(len(item_data), 0)
        self.assertEqual(style, [])

        # Add items
        invoice.add_item(Item('Item1', 'Item desc', 1, 1.1))
        invoice.add_item(Item('Item2', 'Item desc', 2, u'2.2'))
        invoice.add_item(Item(u'Item3', 'Item desc', 3, '3.3'))
        # set tax rate
        invoice.set_item_tax_rate(19)

        # After add items
        items = invoice.items
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].name, 'Item1')
        self.assertEqual(items[0].amount, Decimal('1.1'))
        self.assertEqual(items[1].amount, Decimal('4.4'))
        self.assertEqual(items[2].name, u'Item3')
        self.assertEqual(items[2].amount, Decimal('9.9'))

        item_data, item_subtotal = invoice._item_raw_data_and_subtotal()
        self.assertEqual(item_subtotal, Decimal('15.4'))
        self.assertEqual(len(item_data), 3)

        item_data, style = invoice._item_data_and_style()
        self.assertEqual(len(item_data), 7)  # header, subtotal, tax, total
        self.assertEqual(item_data[-3][-1], Decimal('15.4'))  # subtotal
        self.assertEqual(item_data[-2][-1], Decimal('2.926'))  # tax
        self.assertEqual(item_data[-1][-1], Decimal('18.326'))  # total

        invoice.finish()

        self.assertTrue(os.path.exists(invoice_path))