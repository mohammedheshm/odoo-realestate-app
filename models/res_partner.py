from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_id = fields.Many2one('property')
    # with related field
    price = fields.Float(related='property_id.selling_price')

    # with compute field
    # price = fields.Float(compute='_compute_price')

    # @api.depends('property_id')
    # def _compute_price(self):
    #     for rec in self:
    #         rec.price = rec.property_id.selling_price
    #
