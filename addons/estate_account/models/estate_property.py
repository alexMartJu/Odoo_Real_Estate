# -*- coding: utf-8 -*-

from odoo import models, fields, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True, copy=False)

    def action_sold(self):
        # Call the original action_sold method
        result = super().action_sold()

        # Create an invoice when the property is sold
        for prop in self:
            if prop.state != 'sold':
                continue
            if not prop.buyer_id:
                continue
            if prop.invoice_id:
                continue
            
            # Prepare invoice values
            values = {
                'partner_id': prop.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Commission for property %s' % prop.name,
                        'quantity': 1,
                        'price_unit': prop.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),
                ],
            }

            prop.invoice_id = self.env['account.move'].create(values)

        return result
