from odoo import models, fields

class Website(models.Model):
    _inherit = 'website'
  
    shop_type = fields.Selection(
        [
            ('b2c', 'B2C - Privatkunden-Shop'), ('b2b', 'B2B - Buisnesskunden-Shop')
        ], 
        string='Shoop Type', 
        default='b2c',
        help="Chose the Buisness Type B2C or B2B"
    )
    