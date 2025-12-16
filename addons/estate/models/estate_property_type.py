# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Name", required=True)

    # Constraints
    _unique_type_name = models.Constraint('UNIQUE(name)', 'The property type name must be unique.')
