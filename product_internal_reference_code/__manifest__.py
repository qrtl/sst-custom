# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Product Internal Reference Code',
    'version': '11.0.1.0.0',
    'category': 'Sales',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'depends': [
        'product',
    ],
    'description': """ 
    - When product is created, the system should auto-generate a sequential number 
    for default_code
    - Pre-fix (just pre-fix field) should depend on company (we may add a field in 
    res.company for this purpose)

    An example of generated number: A00023 ("A" from the company dependent pre-fix,
    and "00023" from number_next_actual of ir.sequence)

    """,
    'summary': """ 
        Product is created, system will auto-generate a sequential number for 
        default_code based on company configuration.
    """,
    'data': [
        'data/product_data.xml',
        'views/company_view.xml',
    ],
    'application': False,
    'installable': True,
}
