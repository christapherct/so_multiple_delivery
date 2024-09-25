from odoo import models, fields, api
from collections import defaultdict


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    picking_ids_custom = fields.One2many('stock.picking', 'sale_order_id', string="Custom Delivery Orders")

    picking_count = fields.Integer(string="Custom Delivery Count", compute="_compute_custom_picking_count")

    @api.depends('picking_ids_custom')
    def _compute_custom_picking_count(self):
        for order in self:
            order.picking_count = self.env['stock.picking'].search_count([('sale_order_id', '=', order.id)])

    def action_view_deliveries(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Delivery Orders',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'target': 'current',
            'domain': [('sale_order_id', '=', self.id)],
            'context': dict(self.env.context, create=False),
        }

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.picking_ids.unlink()
        self.create_multiple_deliveries()
        return res

    def create_multiple_deliveries(self):
        product_lines = defaultdict(lambda: {'qty': 0.0, 'uom': None})

        for line in self.order_line:
            product_id = line.product_id.id
            product_lines[product_id]['qty'] += line.product_uom_qty
            product_lines[product_id]['uom'] = line.product_uom

        for product_id, values in product_lines.items():
            self._create_delivery_order(product_id, values['qty'], values['uom'])

    def _create_delivery_order(self, product_id, qty, uom):
        picking_type = self.env.ref('stock.picking_type_out')
        sale_order_id = self.id
        picking = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'picking_type_id': picking_type.id,
            'origin': self.name,
            'sale_order_id': sale_order_id,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': self.partner_id.property_stock_customer.id,
        })
        self.env['stock.move'].create({
            'name': self.env['product.product'].browse(product_id).display_name,
            'product_id': product_id,
            'product_uom_qty': qty,
            'product_uom': uom.id,
            'picking_id': picking.id,
            'location_id': picking.location_id.id,
            'location_dest_id': picking.location_dest_id.id,
            'sale_line_id': False,
        })