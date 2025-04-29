from odoo import models, fields

class Website(models.Model):
    _inherit = 'website'
  
    shop_type = fields.Selection(
        [
            ('b2c', 'B2C - Privat CLients Shop'), ('b2b', 'B2B - Buisness Clients Shop ')
        ], 
        string='Shop Type', 
        default='b2c',
        help="Chose the Shop Type B2C or B2B"
    )
    