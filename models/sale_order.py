from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one('property')
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        print("Inside Action Confirm  Method!")
        return res
