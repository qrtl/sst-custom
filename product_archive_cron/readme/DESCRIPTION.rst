This module does the following:

* A cron task that will "Archive" products which have met certain conditions.

  - Target products to "Archive": The product has to be a Stockable product and (virtual_available + quantity requested in draft purchase.order) <= 0
