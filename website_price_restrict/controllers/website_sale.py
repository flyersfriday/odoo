# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):

    def shop(self, page=0, category=None, search='', min_price=0.0,
             max_price=0.0, ppg=False, **post):
        res = super().shop(page, category, search, min_price,
                           max_price, ppg, **post)
        res.qcontext.update({
            'login_user': False if request.session.uid is None else True
        })
        return res

    def _prepare_product_values(self, product, category, search, **kwargs):
        res = super(WebsiteSaleInherit, self)._prepare_product_values(product,
                                                                      category,
                                                                      search,
                                                                      **kwargs)
        res.update({
            'login_user': False if request.session.uid is None else True
        })
        return res
