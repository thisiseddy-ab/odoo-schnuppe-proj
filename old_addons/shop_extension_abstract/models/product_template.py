from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"
    '''
    def _force_virtual_model(self):
        self.env['product.template.virtual']._name
    '''