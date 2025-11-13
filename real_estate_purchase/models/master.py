from odoo import models, fields, api
from odoo.exceptions import UserError

class RealEstateShippingMethod(models.Model):
    _name = 'rs.shipping.method'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Real Estate Shipping Method'
    _rec_name = 'name'
    _order = 'create_date'

    name = fields.Char(string="Name", required=True, tracking=True)
    code = fields.Char(string="Code", required=True, tracking=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)