from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    shop_visibility = fields.Selection(
        [
            ('b2c', 'B2C - Privat CLients Shop'), ('b2b', 'B2B - Buisness Clients Shop '), ('both', 'Both')
        ], 
        string='Shop Vsibility', 
        default='b2c',
        required=True,
        help="Chose the Shop Visibility Type B2C, B2B or Both"
    )