from odoo import api, models, fields

class ReportGRN(models.AbstractModel):
    _name = 'report.stock_picking_grn.report_grn'
    _description = 'Goods Receipt Note Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'stock.picking',
            'docs': docs,
        }

