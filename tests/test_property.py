from odoo.tests.common import TransactionCase
from odoo import fields


class TestProperty(TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.property_01_record = self.env['property'].create({
            'ref': 'PRT1000',
            'name': 'Property 1000',
            'description': 'Property 1000 description',
            'postcode': '1010',
            'date_availability': fields.Date.today(),
            'bedrooms': 10,
            'expected_price': 10000,
        })

    def test_01_property_values(self):
        self.assertRecordValues(self.property_01_record, [{
            'ref': 'PRT1000',
            'name': 'Property 1000',
            'description': 'Property 1000 description',
            'postcode': '1010',
            'date_availability': fields.Date.today(),
            'bedrooms': 10,
            'expected_price': 10000,
        }])
