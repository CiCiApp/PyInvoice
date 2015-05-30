from __future__ import unicode_literals


class PDFInfo(object):
    def __init__(self, title=None, author=None, subject=None):
        self.title = title
        self.author = author
        self.subject = subject
        self.creator = 'PyInvoice (https://ciciapp.com/pyinvoice)'


class InvoiceInfo(object):
    """
    Invoice information
    """
    def __init__(self, invoice_id, invoice_datetime, due_datetime):
        self.invoice_id = invoice_id
        self.invoice_datetime = invoice_datetime
        self.due_datetime = due_datetime


class AddressInfo(object):
    def __init__(self, name, street, city, state, country, post_code):
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.post_code = post_code


class ServiceProviderInfo(AddressInfo):
    """
    Service provider/Merchant information
    """
    def __init__(self, name, street, city, state, country, post_code):
        super(ServiceProviderInfo, self).__init__(name, street, city, state, country, post_code)


class ClientInfo(AddressInfo):
    """
    Client/Custom information
    """
    def __init__(self, email, client_id, name, street, city, state, country, post_code):
        super(ClientInfo, self).__init__(name, street, city, state, country, post_code)
        self.email = email
        self.client_id = client_id


class Item(object):
    """
    Product/Item information
    """
    def __init__(self, item_id, name, description, units, unit_price):
        """
        Item modal init
        :param item_id: Order id or Item id
        :param name: Item name
        :param units: Amount
        :param unit_price: Unit price
        :return:
        """
        # TODO: add vat/tax, subtotal
        self.item_id = item_id
        self.name = name
        self.description = description
        self.units = units
        self.unit_price = unit_price

    @property
    def subtotal(self):
        return int(self.units) * self.unit_price


class Transaction(object):
    """
    Transaction information
    """
    def __init__(self, gateway, transaction_id, transaction_datetime, amount):
        self.gateway = gateway
        self.transaction_id = transaction_id
        self.transaction_datetime = transaction_datetime
        self.amount = amount