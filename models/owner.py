from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(required=1)
    phone = fields.Char()
    address = fields.Char()
    property_ids = fields.One2many('property', 'owner_id')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!'),
    ]
