# Sales Data Import

This module provides following functions:

- Imports sales data of designated format from `.csv` file (with UTF-8 encoding), and
  processes following transactions:
- Sales Order
- Availability check on outgoing picking
- Customer Invoice
- Customer Payment

This module depends on `base_import_log` and `queue_job` modules.

# Installation

- Place this module and `base_import_log` module in your addons directory, update the
  module list in Odoo, and install this module. `base_import_log` module should be
  automatically installed when you install this module.

# Configuration

- User should belong to 'Data Import' group. Adjust the user access right settings from
  `Settings > Users > (the user) > Access Rights > Technical Settings`.
- Select default journals ('Invoice Journal' and 'Payment Journal') in "Sales Import
  Defaults" screen. The values are used to propose journals in "Sales Data Import"
  wizard.
- Selece default 'Shipping Policy' and 'Create Invoice' in "Sales Import Defaults"
  screen. If 'On Delivery Order' or 'Create Invoice' is selected, customer invoice and
  payment will not be created.
- Set Implementation of Customer Invoices sequence to "Standard" (instead of "No Gap".
  Queue jobs seem to fail for not being able to obtain lock on ir_sequence row.

# Usage

Go to `Import > Import > Import Sales Order` to import sales data in `.csv` format.

Go to `Import > Data Import Log > Import Log` to find the import history / error log.

## Program Logic

- The first line of the import file is field labels shown as follows:
- 'Group'
- 'Line Product'
- 'Line Description'
- 'Line Unit Price'
- 'Line Qty'
- 'Line Tax'
- 'Customer'
- 'Pricelist'
- 'Warehouse'
- 'Notes'
- Records for import should be prepared from the second line onwards.
- "Group" values should be used to separate sales orders.
- Products are identified based on "Internal Reference" (`default_code`).
- Customers are identified based on "Name".
- Negative values are not allowed for "Unit Price" and "Qty" fields of the import file.
- Sales order currency is determined based on the selected "Pricelist".
- If "Line Description" is left blank, the system proposes a description according to
  the standard logic (i.e. "Internal Reference" + "Name" of the product).
- For document level fields (Customer, Pricelist, Notes, Warehouse, etc.), the program
  only looks at the first record in the same "Group" and ignore the rest (there will be
  no error even if there is inconsistency - e.g. different Customers for the same SO).
- The program should not create any record if there is an error in any of the record.
  User is expected to find the error content in the error log, correct all the errors in
  the import file, and re-import it.
