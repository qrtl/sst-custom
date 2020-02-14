# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Product Publish Cron',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Extra Tools',
    'license': "AGPL-3",
    'description': """
A cron task that will publish products with custom domain and values.
    """,
    'summary': """""",
    'depends': [
        'stock_ext_sst',
    ],
    'data': [
        'data/cron_data.xml',
    ],
    'installable': True,
}
