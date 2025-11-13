.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.html
   :alt: License: AGPL-3

Website Price Hide for Non Logged-In Users
==========================================

This module hides product prices, quantity, and the "Add To Cart" button from non logged-in (guest) users on the website.
Only logged-in users can see product prices and make purchases.

Features
========
* Hide product price for guest users on the website.
* Hide quantity field and "Add To Cart" button for non logged-in users.
* Logged-in users can:
  - View product prices.
  - See available quantities.
  - Add products to the cart and proceed to checkout.
* Fully integrated with Odoo’s Website and eCommerce modules.

Use Case
========
This is ideal for B2B or restricted-access eCommerce websites where prices should only be visible to registered users or customers.

Configuration
=============
1. Install the module **Website Price Hide for Non Logged-In Users**.
2. No extra configuration is required.
3. Log out of your account and open the shop page — prices and cart buttons will be hidden.
4. Log back in to confirm that product prices and cart access are visible.

Technical Details
=================
* **Module Name:** `website_price_restrict`
* **Version:** 17.0
* **Depends on:** `website_sale`
* **Assets:** Custom SCSS to manage frontend styling and visibility

License
-------
This module is licensed under the **AGPL-3 License**.
See https://www.gnu.org/licenses/agpl-3.0.html for details.

Author
------
**For**

Maintainer
-----------
This module is maintained by **Flyers Friday Team**.
For issues or contributions, please visit:
`Flyers Friday GitHub <https://github.com/flyersfriday>`__

Contact
-------
📧 **Email:** flyersfriday@gmail.com
🌐 **Website:** https://github.com/flyersfriday

Further Information
===================
* HTML Description: `<static/description/index.html>`__
