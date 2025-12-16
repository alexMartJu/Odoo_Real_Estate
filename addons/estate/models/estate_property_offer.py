# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    # Constraints
    _check_offer_price = models.Constraint('CHECK(price > 0)', 'The offer price must be strictly positive.')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    # Action buttons
    def action_accept(self):
        for record in self:
            prop = record.property_id
            # Check if another offer has already been accepted for this property
            other_accepted = prop.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != record.id)
            if other_accepted:
                raise UserError('Another offer has already been accepted for this property.')
            record.status = 'accepted'
            # Set property's selling price and buyer
            prop.selling_price = record.price
            prop.buyer_id = record.partner_id
            prop.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for record in self:
            was_accepted = (record.status == 'accepted')
            record.status = 'refused'
            if was_accepted:
                # If we refuse an already accepted offer, clear property's buyer/selling_price
                prop = record.property_id
                prop.selling_price = 0.0
                prop.buyer_id = False
                prop.state = 'new'
        return True
