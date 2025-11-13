from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    grn_number = fields.Char(string="GRN Number", readonly=True, store=True, copy=False)
    date_of_receipt = fields.Date(string="Date of Receipt", default=fields.Date.context_today)
    po_number = fields.Char(string="PO Number", compute="_compute_po_number", store=True)
    invoice_id = fields.Many2one('account.move', string="Vendor Bill", readonly=True)

    supplier_id = fields.Many2one('res.partner', string="Supplier")
    buyer_id = fields.Many2one('res.partner', string="Buyer")

    # Transportation Details
    transport_mode = fields.Selection([
        ('truck', 'Truck'),
        ('air', 'Air'),
        ('ship', 'Ship'),
        ('rail', 'Rail'),
        ('other', 'Other'),
    ], string="Transport Mode", default='truck')
    driver_name = fields.Char(string="Driver Name")
    vehicle_number = fields.Char(string="Vehicle Number")
    transport_company = fields.Char(string="Transport Company")

    # Inspection
    received_by = fields.Many2one('res.partner', string="Received & Inspected By")
    supplier_representative = fields.Many2one('res.partner', string="Supplier Representative")

    @api.depends('origin')
    def _compute_po_number(self):
        for picking in self:
            po = self.env['purchase.order'].search([('name', '=', picking.origin)], limit=1)
            picking.po_number = po.name if po else picking.origin

    @api.model_create_multi
    def create(self, vals_list):
        pickings = super().create(vals_list)
        for picking in pickings:
            if not picking.grn_number:
                picking.grn_number = self.env['ir.sequence'].next_by_code('stock.picking.grn') or '/'
        return pickings

    def button_validate(self):
        """Override validation to auto-link GRN with Vendor Bill if PO exists"""
        res = super().button_validate()
        for picking in self:
            purchase_order = self.env['purchase.order'].search([('name', '=', picking.origin)], limit=1)
            if purchase_order:
                # Link GRN to existing invoice if any
                invoice = self.env['account.move'].search([
                    ('invoice_origin', '=', purchase_order.name),
                    ('move_type', '=', 'in_invoice')
                ], limit=1)
                if invoice:
                    picking.invoice_id = invoice
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    batch_number = fields.Char(string="Batch Number")
    condition = fields.Selection([
        ('good', 'Good'),
        ('damaged', 'Damaged'),
        ('expired', 'Expired'),
        ('other', 'Other'),
    ], string="Condition", default='good')
    qty_ordered = fields.Float(string="Qty Ordered")
    qty_rejected = fields.Float(string="Qty Rejected")
    qty_received = fields.Float(string="Qty Received")

    class StockMove(models.Model):
        _inherit = 'stock.move'

        batch_number = fields.Char(string="Batch Number")
        condition = fields.Selection([
            ('good', 'Good'),
            ('damaged', 'Damaged'),
            ('expired', 'Expired'),
            ('other', 'Other'),
        ], string="Condition", default='good')
        qty_ordered = fields.Float(string="Qty Ordered")
        qty_rejected = fields.Float(string="Qty Rejected")
        qty_received = fields.Float(string="Qty Received", readonly=True)

        @api.onchange('product_uom_qty', 'quantity', 'qty_rejected')
        def _onchange_qtys(self):
            for line in self:
                # Ordered Qty
                line.qty_ordered = line.product_uom_qty

                # Received = Total Done - Rejected
                line.qty_received = max(line.quantity - line.qty_rejected, 0)
