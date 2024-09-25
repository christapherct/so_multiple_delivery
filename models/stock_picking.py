from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'stock.picking'

    sale_order_id = fields.Many2one('sale.order')