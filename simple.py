from datetime import datetime
from decimal import Decimal

from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item, Transaction
from pyinvoice.templates import SimpleInvoice


doc = SimpleInvoice('test.pdf')

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
doc.set_item_tax_rate(20)  # 20%

doc.add_transaction(Transaction('Paypal', 111, datetime.now(), 1))
doc.add_transaction(Transaction('Strip', 222, datetime.now(), 2))

doc.finish()