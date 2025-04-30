from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo import http
from odoo.http import request

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
        product_template = request.env['product.template'].browse(
            product_template_id and int(product_template_id)
        )

        combination_values = request.env['product.template.attribute.value'].browse(combination)
        parent_combination_values = request.env['product.template.attribute.value'].browse(parent_combination)

        # ✅ Compute the combination info
        combination_info = product_template._get_combination_info(
            combination=combination_values,
            product_id=product_id and int(product_id),
            add_qty=add_qty and float(add_qty) or 1.0,
            parent_combination=parent_combination_values,
        )

        # ✅ Keep a copy before popping for template rendering
        full_combination_info = combination_info.copy()

        # ⚠ Strip backend-only fields before returning to client
        for key in ('product_taxes', 'taxes', 'currency', 'date', 'combination'):
            combination_info.pop(key, None)

        # ✅ Inject filtered variant HTML
        combination_info['variant_html'] = request.env['ir.ui.view']._render_template(
            'shop_extension_pr_vr.filtered_variants_template',  # Replace with your module.template ID
            values={
                'product': product_template,
                'parent_combination': parent_combination_values if parent_combination else None,
                'combination': combination_values,
                'ul_class': 'flex-column',
                'combination_info': full_combination_info,  # Needed for badge_extra_price!
            }
        )

        # ✅ Carousel (images)
        if request.website.product_page_image_width != 'none' and not request.env.context.get('website_sale_no_images', False):
            combination_info['carousel'] = request.env['ir.ui.view']._render_template(
                'website_sale.shop_product_images',
                values={
                    'product': product_template,
                    'product_variant': request.env['product.product'].browse(combination_info['product_id']),
                    'website': request.env['website'].get_current_website(),
                },
            )

        # ✅ Product tags
        product = request.env['product.product'].browse(combination_info['product_id'])
        if product and request.website.is_view_active('website_sale.product_tags'):
            combination_info['product_tags'] = request.env['ir.ui.view']._render_template(
                'website_sale.product_tags', values={
                    'all_product_tags': product.all_product_tag_ids.filtered('visible_on_ecommerce')
                }
            )

        return combination_info
    
    '''
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
                'price': 0.0,
                'display_price': '0.00',
                'list_price': 0.0,
                'has_discounted_price': False,
                'can_be_sold': False,
            })
        return response
    '''

