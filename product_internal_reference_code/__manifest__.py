# -*- coding: utf-8 -*-
#    OpenERP, Open Source Management Solution
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

{
    'name': 'Product Internal Reference Code',
    'category': 'Sales',
    'version': '1.0',
    'author': 'Rooms For (Hong Kong) T/A OSCG',
    'depends': ['product'],
    'website': 'www.openerp-asia.net',
    'description': """ 
- When product is created, the system should auto-generate a sequential number for default_code
- Pre-fix (just pre-fix field) should depend on company (we may add a field in res.company for this purpose)

An example of generated number: A00023 ("A" from the company dependent pre-fix, and "00023" from number_next_actual of ir.sequence)

    """,
    'summary':""" 
        Product is created, system will auto-generate a sequential number for default_code based on company configuration.
    """,
    'data': [
            'data/product_sequence.xml',
            'views/company_view.xml',
             ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
