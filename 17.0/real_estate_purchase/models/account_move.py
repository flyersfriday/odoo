from odoo import api, models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    grn_ids = fields.One2many('stock.picking', 'invoice_id', string="Related GRNs")
    grn_count = fields.Integer(string="GRN Count", compute="_compute_grn_count")
    purchase_order = fields.Many2one('purchase.order', string="Purchase Order")

    def _compute_grn_count(self):
        for move in self:
            move.grn_count = len(move.grn_ids)

    @api.model
    def action_post(self):
        res = super(AccountMove, self).action_post()

        for move in self:
            # Only handle Vendor Bills
            if move.move_type == 'in_invoice':
                # Link to related pickings through PO (if exists)
                purchase_orders = move.invoice_line_ids.mapped('purchase_line_id.order_id')
                pickings = purchase_orders.mapped('picking_ids').filtered(lambda p: p.state != 'cancel')

                # If not found through PO, try manual match (optional)
                if not pickings and move.ref:
                    pickings = self.env['stock.picking'].search([('origin', '=', move.ref)])

                for picking in pickings:
                    picking.invoice_id = move.id

        return res
