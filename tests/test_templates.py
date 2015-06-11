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

        # test style
        # ## Subtotal
        self.assertEqual(style[-4], ('SPAN', (0, 4), (3, 4)))
        self.assertEqual(style[-3], ('ALIGN', (0, 4), (-2, -1), 'RIGHT'))
        # ## Total
        self.assertEqual(style[-2], ('SPAN', (0, 5), (3, 5)))
        self.assertEqual(style[-1], ('ALIGN', (0, 5), (-2, -1), 'RIGHT'))

        invoice.finish()

        self.assertTrue(os.path.exists(invoice_path))

    def test_only_items_with_tax_rate(self):
        invoice_path = os.path.join(self.file_base_dir, 'only_items_with_tax.pdf')
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

    def test_invoice_info(self):
        invoice_path = os.path.join(self.file_base_dir, 'invoice_info.pdf')
        if os.path.exists(invoice_path):
            os.remove(invoice_path)

        invoice = SimpleInvoice(invoice_path)

        # Before add invoice info
        invoice_info_data = invoice._invoice_info_data()
        self.assertEqual(invoice_info_data, [])

        invoice.invoice_info = InvoiceInfo(12)

        # After add invoice info
        invoice_info_data = invoice._invoice_info_data()
        self.assertEqual(len(invoice_info_data), 1)
        self.assertEqual(invoice_info_data[0][0], 'Invoice id:')
        self.assertEqual(invoice_info_data[0][1], 12)

        invoice.invoice_info = InvoiceInfo(12, invoice_datetime=datetime(2015, 6, 1))
        invoice_info_data = invoice._invoice_info_data()
        self.assertEqual(len(invoice_info_data), 2)
        self.assertEqual(invoice_info_data[1][0], 'Invoice date:')
        self.assertEqual(invoice_info_data[1][1], '2015-06-01 00:00')

        invoice.finish()

        self.assertTrue(os.path.exists(invoice_path))

    def test_service_provider_info(self):
        invoice_path = os.path.join(self.file_base_dir, 'service_provider_info.pdf')
        if os.path.exists(invoice_path):
            os.remove(invoice_path)

        invoice = SimpleInvoice(invoice_path)

        # Before add service provider info
        info_data = invoice._service_provider_data()
        self.assertEqual(info_data, [])

        # Empty info
        invoice.service_provider_info = ServiceProviderInfo()
        info_data = invoice._service_provider_data()
        self.assertEqual(info_data, [])

        invoice.service_provider_info = ServiceProviderInfo(
            name='CiCiApp',
            street='Street xxx',
            city='City ccc',
            state='State sss',
            country='Country rrr',
            post_code='Post code ppp',
            vat_tax_number=666
        )

        # After add service provider info
        info_data = invoice._service_provider_data()
        self.assertEqual(len(info_data), 7)
        self.assertEqual(info_data[0][0], 'Name:')
        self.assertEqual(info_data[0][1], 'CiCiApp')
        self.assertEqual(info_data[4][0], 'Country:')
        self.assertEqual(info_data[4][1], 'Country rrr')
        self.assertEqual(info_data[6][0], 'Vat/Tax number:')
        self.assertEqual(info_data[6][1], 666)

        invoice.finish()

        self.assertTrue(os.path.exists(invoice_path))

    def test_client_info(self):
        invoice_path = os.path.join(self.file_base_dir, 'client_info.pdf')
        if os.path.exists(invoice_path):
            os.remove(invoice_path)

        invoice = SimpleInvoice(invoice_path)

        # Before add client info
        info_data = invoice._client_info_data()
        self.assertEqual(info_data, [])

        # Empty info
        invoice.client_info = ClientInfo()
        info_data = invoice._client_info_data()
        self.assertEqual(info_data, [])

        invoice.client_info = ClientInfo(
            name='Client ccc',
            street='Street sss',
            city='City ccc',
            state='State sss',
            country='Country ccc',
            post_code='Post code ppp',
            email='Email@example.com',
            client_id=3214
        )

        # After add client info
        info_data = invoice._client_info_data()
        self.assertEqual(len(info_data), 8)
        self.assertEqual(info_data[0][0], 'Name:')
        self.assertEqual(info_data[0][1], 'Client ccc')
        self.assertEqual(info_data[6][0], 'Email:')
        self.assertEqual(info_data[6][1], 'Email@example.com')
        self.assertEqual(info_data[7][0], 'Client id:')
        self.assertEqual(info_data[7][1], 3214)

        invoice.finish()

        self.assertTrue(os.path.exists(invoice_path))

    def test_transaction(self):
        invoice_path = os.path.join(self.file_base_dir, 'transaction.pdf')
        if os.path.exists(invoice_path):
            os.remove(invoice_path)

        invoice = SimpleInvoice(invoice_path)

        transaction_data = invoice._transactions_data()
        self.assertEqual(transaction_data, [])

        invoice.add_transaction(Transaction('A', 1, date.today(), 9.9))
        invoice.add_transaction(Transaction('B', 3, date(2015, 6, 1), 3.3))

        transaction_data = invoice._transactions_data()
        self.assertEqual(len(transaction_data), 3)
        self.assertEqual(transaction_data[0][0], 'Transaction id')
        self.assertEqual(transaction_data[1][3], 9.9)
        self.assertEqual(transaction_data[2][0], 3)
        self.assertEqual(transaction_data[2][2], '2015-06-01')
        self.assertEqual(transaction_data[2][3], 3.3)

        invoice.finish()

        self.assertTrue(os.path.exists(invoice_path))
