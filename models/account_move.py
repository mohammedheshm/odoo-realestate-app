from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'account.move'

    def action_do_somthing(self):
        print(self,"inside action_do_somthing")
