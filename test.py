from datetime import datetime
from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo
from pyinvoice.templates import SimpleInvoice

doc = SimpleInvoice('test.pdf')
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

# doc.build(story, onFirstPage=PaidStamp(7*inch, 5.8*inch))
doc.finish()