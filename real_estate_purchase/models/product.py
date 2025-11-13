from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_real_estate = fields.Boolean(string="Is Real Estate Product")

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_real_estate = fields.Boolean(string="Is Real Estate Product")
