from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default='New', readonly=1)
    name = fields.Char(required=1, default='New', size=50, translate=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff')
    bedrooms = fields.Integer(required=1)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(groups="app_one.property_manager_group")
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_phone = fields.Char(related='owner_id.phone', readonly=0)
    owner_address = fields.Char(related='owner_id.address', readonly=0)
    create_time = fields.Datetime(default=fields.Datetime.now())
    next_time = fields.Datetime(compute='_compute_next_time')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!'),
    ]

    lines_ids = fields.One2many('property.line', 'property_id')
    active = fields.Boolean(default=True)

    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            # print(rec)
            # print("inside _computed_diff method")
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print(rec)
            # print("inside _onchange_expected_price method")
            return {
                'warning': {'title': 'warning', 'message': 'negative value.', 'type': 'notification'}
            }

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please Add Valid Number of Bedrooms!')

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'
            # rec.write({
            #     'state':'draft'
            # })

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            # print("inside pending action")
            rec.write({  # = rec.state='pending'
                'state': 'pending'
            })

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            # print("inside sold action")
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            # print("inside closed action")
            rec.state = 'closed'

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True

    def action(self):
        # print(self.env.user.login)
        # print(self.env.user.name)
        # print(self.env.user.id)
        # print(self.env.uid)
        # print(self.env.company)
        # print(self.env.company.name)
        # print(self.env.company.id)
        # print(self.env.company.street)
        # print(self.env.context)
        # print(self.env.cr)
        # print(self.env['owner'].create({
        #     'name': 'name two',
        #     'phone': '01000000000000000',
        # }))

        # owners = self.env['owner'].search([('name', '=', 'name two')])
        # owners.write({
        #     'phone': '01111111111111',
        #     'name': 'Updated Name',
        # })

        # write2 = self.env['owner'].search([('name', '=', 'name one')])
        # write2.write({
        #     'name': 'update name2',
        #     'phone': '55555555555555'
        # })

        print(self.env['property'].search(['&', ('name', '!=', 'property1'), ('postcode', '!=', '985')]))
        # delete1.unlink()

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area}) for line in rec.lines_ids]
            })

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

    def get_properties(self):
        payload = dict()
        try:
            response = requests.get('http://localhost:8069/v1/properties', data=payload)
            if response.status_code == 200:
                # data = response.json()
                # print(data)
                print("Successful")
            else:
                print("Fail")
        except Exception as error:
            raise ValidationError(str(error))

class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()
