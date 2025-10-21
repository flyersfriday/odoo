# -*- coding: utf-8 -*-
###############################################################################
#
#    Flyers Friday
#
#    Copyright (C) 2023-TODAY Flyers Friday (<https://github.com/flyersfriday>)
#    Author: Flyers Friday Development Team (flyersfriday@gmail.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    "name": "Real Estate Purchase",
    "version": "1.0.0",
    "summary": "Create POs from Real Estate records - map lines to purchase.order",
    "category": "Custom",
    "author": "Flyers Friday",
    "license": "LGPL-3",
    'images': ['static/description/banner.jpg'],
    "depends": ["base", "product", "stock", "account", "purchase"],
    "data": [
        "data/sequence.xml",
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/purchase_order_view.xml",
        "views/real_estate_views.xml",
        "views/stock_picking_views.xml",
        "views/master_views.xml",
        "views/menu_views.xml",
        "reports/real_estate_purchase_order_templates.xml",
        "reports/real_estate_purchase_order_report.xml",
        'reports/report_grn.xml',
    ],
    "installable": True,
    "application": False
}
