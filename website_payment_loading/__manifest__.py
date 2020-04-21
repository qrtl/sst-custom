# Copyright 2018 Soliton Systems
# Copyright 2018 Alliance Software Inc.
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Payment Loading Screen",
    "version": "11.0.1.0.0",
    "author": "Soliton Systems," "Alliance Software Inc.," "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Payment",
    "license": "AGPL-3",
    "description": """
    This module modify the payment page, add a loading screen after user presses
    the "Pay Now" button. This module might not be fully compactible with
    payment acquirers using JS functions to do the checkout, e.g. Stripe.

    Attribution: the main parts of the code were extracted from a module
    developed by Soliton and Alliance, and were adjusted by Quartile.
        """,
    "depends": ["payment"],
    "data": ["views/templates.xml"],
    "installable": True,
}
