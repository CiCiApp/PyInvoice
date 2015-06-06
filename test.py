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
    post_code='My Post code'
)

doc.client_info = ClientInfo(
    email='My Email',
    client_id='My Client Id',
    name='Client Name',
    street='Client Street',
    city='Client City',
    state='Client State',
    country='Client country',
    post_code='Client Post code'
)

doc.add_item(Item('0000', 'Item 0000', 'Item Description 1 Long--------------------------------Item Description 1 Long', 1, Decimal('1.1')))
doc.add_item(Item('1111', 'Item 1111', 'Item Description 2', 2, Decimal('2.2')))
doc.add_item(Item('2222', 'Item 2222', 'Item Description 3', 3, Decimal('3.3')))

doc.add_transaction(Transaction('Paypal', 111, datetime.now(), 1))
doc.add_transaction(Transaction('Strip', 222, datetime.now(), 2))

doc.finish()