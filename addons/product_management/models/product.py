from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    ### Custom Fields ###
    shop_visibility = fields.Boolean(
        String="Shoop Visibility", 
        default=False,
        help="Chose is it should be visible in Shop Front End"
    )
    
    buisness_type = fields.Selection(
        [
            ('b2c', 'B2C - Privatkunden-Shop'), ('b2b', 'B2B - Buisnesskunden-Shop')
        ], 
        string='Buisness Type', 
        default='b2c',
        help="Chose the Buisness Type B2C or B2B"
    )
    