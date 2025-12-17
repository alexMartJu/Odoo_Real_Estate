# -*- coding: utf-8 -*-

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Relations
    property_ids = fields.One2many(
        'estate.property', 'salesperson_id', string='Properties',
        domain=[('state', 'in', ['new', 'offer_received'])]
    )
