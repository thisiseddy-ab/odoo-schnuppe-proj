from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo import http

'''
## Test Log##
import logging
_logger = logging.getLogger(__name__)
'''


class WebsiteSaleVariantControllerExtend(WebsiteSaleVariantController):

    @http.route('/website_sale/get_combination_info', type='json', auth='public', methods=['POST'], website=True)
    def get_combination_info_website(
        self, product_template_id, product_id, combination, add_qty, parent_combination=None, **kwargs
    ):
        website = http.request.env['website'].get_current_website()
        shop_type = website.shop_type

        # Call the original method
        response = super().get_combination_info_website(
            product_template_id, product_id, combination, add_qty, parent_combination, **kwargs
        )

        # Get the variant and check visibility
        variant_id = response.get('product_id')
        variant = http.request.env['product.product'].browse(variant_id) if variant_id else None

        if not variant or not variant.exists() or variant.shop_visibility not in [shop_type, 'both']:
            response.update({
                'not_available': True,
                'error': "This combination is not available in this shop.",
                'product_id': False,
                'is_combination_possible': False,
                # Optionally zero out the price
                'price': 0.0,
                'display_price': '0.00',
                'list_price': 0.0,
                'has_discounted_price': False,
                'can_be_sold': False,
            })
        return response