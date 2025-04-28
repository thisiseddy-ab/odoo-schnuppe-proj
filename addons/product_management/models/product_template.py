from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ### Custom Fields ###
    shop_visibility = fields.Boolean(
        String="Shoop Visibility", 
        default=False,
        help="Chose is it should be visible in Shop Front End"
    )
    
    shop_type = fields.Selection(
        [
            ('b2c', 'B2C - Privatkunden-Shop'), ('b2b', 'B2B - Buisnesskunden-Shop')
        ], 
        string='Shoop Type', 
        default='b2c',
        help="Chose the Buisness Type B2C or B2B"
    )
    