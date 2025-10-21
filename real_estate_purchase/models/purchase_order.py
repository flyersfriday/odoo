from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    real_estate_id = fields.Many2one('real.estate', string='Real Estate Reference')
    seller_id = fields.Many2one('res.partner', string="Seller (Customer)", required=True,
                                domain=[('customer_rank', '>', 0)])
    shipping_date = fields.Date(string="Shipping Date")

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()

        for order in self:
            for picking in order.picking_ids:
                picking.supplier_id = order.seller_id.id
                picking.buyer_id = order.partner_id.id  # buyer is your company partner

        return res

    def get_tax_name(self):
        """Return unique tax names from order lines (no duplicate percentages)"""
        self.ensure_one()
        tax_names = set()

        for line in self.order_line:
            for tax in line.taxes_id:
                # tax.name already includes the percentage in most setups (e.g. "Sales Tax 15%")
                tax_names.add(tax.name)

        return ', '.join(sorted(tax_names))

    def action_create_invoice(self):
        res = super(PurchaseOrder, self).action_create_invoice()
        # Link PO to created invoice
        for po in self:
            invoice = self.env['account.move'].search([
                ('invoice_origin', '=', po.name),
                ('move_type', '=', 'in_invoice'),
            ], limit=1)
            if invoice:
                invoice.purchase_order = po.id
        return res
