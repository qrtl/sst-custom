This module converts the image attachment to image_1920 field.

Background
~~~~~~~~~~

When we install the attachment_s3 module in older odoo version and migrate
to another odoo version higher than v13.0 using openupgrade, image conversion can't work well
because migration script can't fetch data from s3 during 12.0>13.0 migration. So, we need this
module in final version migration to convert images.
