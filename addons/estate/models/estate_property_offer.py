# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = 'price desc'

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', copy=False)
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', string='Property Type', store=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    # Constraints
    _check_offer_price = models.Constraint('CHECK(price > 0)', 'The offer price must be strictly positive.')

    # Override create to enforce business rules and update property state
    @api.model_create_multi
    def create(self, vals_list):
        Property = self.env['estate.property']

        # Pre-validate incoming offers (vals_list contains dicts with fields)
        for vals in vals_list:
            prop_id = vals.get('property_id')
            price = vals.get('price')
            # Only validate when both property_id and price are present
            if prop_id and price is not None:
                # Use browse(id) to obtain the estate.property record (no extra search)
                prop = Property.browse(prop_id)
                # If the property exists and already has offers, get the maximum
                # existing offer price and compare it with the new price.
                if prop and prop.offer_ids:
                    max_offer = max(prop.offer_ids.mapped('price'))
                    # Business rule: do not allow creating an offer with a price
                    # lower than the current maximum offer for the same property.
                    if price < max_offer:
                        raise ValidationError(
                            'The offer price (%.2f) cannot be lower than the existing maximum offer (%.2f).' % (price, max_offer)
                        )

        # Create offers (call super after validation)
        offers = super().create(vals_list)
        # Update property state to 'offer_received' when previously 'new'
        for offer in offers:
            if offer.property_id and offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'
        return offers

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
