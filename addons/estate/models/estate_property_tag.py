# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(string="Name", required=True)

    # Constraints
    _unique_tag_name = models.Constraint('UNIQUE(name)', 'The tag name must be unique.')
