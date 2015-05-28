from reportlab.lib.units import inch
from pyinvoice.components import SimpleTable, PaidStamp
from pyinvoice.templates import SimpleInvoice

story = []

address_table = SimpleTable([
    ['Name', 'zhangshine'],
    ['City', 'Jining'],
    ['City', 'Jining'],
    ['City', 'Jining'],
    ['City', 'Jining'],
    ['City', 'Jining']
], horizontal_align='RIGHT')
story.append(address_table)

merchant_table = SimpleTable([
    ['Name', 'CiCiApp'],
    ['xxxx', 'yyyy']
], horizontal_align='LEFT')
story.append(merchant_table)

doc = SimpleInvoice('test.pdf')

doc.build(story, onFirstPage=PaidStamp(inch, 10*inch))
