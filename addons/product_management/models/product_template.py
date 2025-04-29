from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ### Custom Fields ###
    shop_visibility = fields.Selection(
        [
            ('b2c', 'B2C - Privat CLients Shop'), ('b2b', 'B2B - Buisness Clients Shop ')
        ], 
        string='Shop Vsibility', 
        default='b2c',
        help="Chose the Shop Visibility Type B2C or B2B"
    )
    