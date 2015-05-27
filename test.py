from pyinvoice.components import AddressTable
from pyinvoice.templates import SimpleInvoice

story = []

address_table = AddressTable([
    ['Name', 'zhangshine'],
    ['City', 'Jining']
], horizontal_align='RIGHT')
story.append(address_table)

doc = SimpleInvoice('test.pdf')

doc.build(story)
