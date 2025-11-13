from odoo import models, fields, api
from odoo.exceptions import UserError

class RealEstate(models.Model):
    _name = 'real.estate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'create_date'
    _description = 'Real Estate'

    name = fields.Char(string="Name", required=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer (Vendor)", required=True, domain=[('supplier_rank', '>', 0)])
    seller_id = fields.Many2one('res.partner', string="Seller (Customer)", required=True, domain=[('customer_rank', '>', 0)])
    shipping_date = fields.Date(string="Shipping Date")
    shipping_method_id = fields.Many2one('rs.shipping.method', string="Shipping Method", required=False)

    line_ids = fields.One2many('real.estate.line', 'real_estate_id', string="Line Items")
    purchase_order_id = fields.Many2one('purchase.order', string="Related Purchase Order", readonly=True)

    def action_confirm_po(self):
        """Generate Purchase Order automatically from real estate lines"""
        PurchaseOrder = self.env['purchase.order']
        for estate in self:
            if not estate.line_ids:
                raise UserError("Please add at least one Real Estate line before confirming.")

            # prepare order lines
            order_lines = []
            for line in estate.line_ids:
                if not line.product_id:
                    raise UserError("Each line must have a product assigned.")
                order_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'product_qty': line.quantity,
                    'product_uom': line.product_id.uom_id.id,
                    'price_unit': line.unit_price,
                    'date_planned': estate.shipping_date or fields.Date.today(),
                }))

            po_vals = {
                'partner_id': estate.buyer_id.id,
                'seller_id': estate.seller_id.id,
                'real_estate_id': estate.id,
                'shipping_date': estate.shipping_date,
                'order_line': order_lines,
            }

            purchase_order = PurchaseOrder.create(po_vals)
            estate.purchase_order_id = purchase_order.id


class RealEstateLine(models.Model):
    _name = 'real.estate.line'
    _description = 'Real Estate Line'

    real_estate_id = fields.Many2one('real.estate', string="Real Estate", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", domain=[('is_real_estate', '=', True)], required=True)
    skn = fields.Char(string="SKN")
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    unit_price = fields.Float(string="Unit Price", required=True)
    amount = fields.Monetary(string="Amount", compute="_compute_amount", store=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id.id)

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Auto set SKU and unit price when product is selected"""
        for line in self:
            if line.product_id:
                # ✅ Force read to ensure standard_price & default_code are loaded
                product = line.product_id.with_context(lang=self.env.user.lang)

                line.skn = product.default_code or ''
                # Use standard_price (cost) if set, else list_price
                price = product.standard_price or product.list_price or 0.0
                line.unit_price = price
            else:
                line.skn = ''
                line.unit_price = 0.0