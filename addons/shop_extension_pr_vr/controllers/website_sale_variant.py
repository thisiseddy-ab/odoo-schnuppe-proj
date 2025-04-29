from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo.http import route, request
from odoo import http

class WebsiteSaleVariantControllerExtend(WebsiteSaleVariantController):

    @route('/website_sale/get_combination_info', type='json', auth='public', methods=['POST'], website=True)
    def get_combination_info_website(
        self, product_template_id, product_id, combination, add_qty, parent_combination=None,
        **kwargs
    ):
        response = super().get_combination_info_website(
            product_template_id, product_id, combination, add_qty, parent_combination, **kwargs
        )

        website = request.env['website'].get_current_website()
        shop_type = website.shop_type

        product = request.env['product.product'].browse(response.get('product_id'))
        if product and product.shop_visibility not in [shop_type, 'both']:
            # Invalidate the combo
            response.update({
                'not_available': True,
                'error': "This combination is not available in this shop.",
                'product_id': False,
                'price': 0.0,
                'can_be_sold': False,
            })

        return response