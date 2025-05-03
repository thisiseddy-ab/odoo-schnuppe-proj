from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo import http

class WebsiteSaleVariantControllerExtend(WebsiteSaleVariantController):
    
    @http.route('/website_sale/get_combination_info', type='json', auth='public', methods=['POST'], website=True)
    def get_combination_info_website(
        self, product_template_id, product_id, combination, add_qty, parent_combination=None, **kwargs
    ):
        request = http.request
        env = request.env
        product_template = env['product.template'].browse(int(product_template_id))
        website = env['website'].get_current_website()

        ptav_ids = env['product.template.attribute.value'].browse(combination or [])
        parent_ptav_ids = env['product.template.attribute.value'].browse(parent_combination or [])
        all_ptavs = ptav_ids | parent_ptav_ids

        candidate_product, ptav_ids = product_template.getVisibleVariant_or_Default(all_ptavs, website)

        combination_info = product_template._get_combination_info(
            combination=ptav_ids,
            product_id=candidate_product.id,
            add_qty=float(add_qty or 1.0),
            parent_combination=parent_ptav_ids,
        )

        for key in ('product_taxes', 'taxes', 'currency', 'date', 'combination'):
            combination_info.pop(key, None)

        combination_info['actual_combination'] = ptav_ids.ids

        if website.product_page_image_width != 'none' and not env.context.get('website_sale_no_images'):
            combination_info['carousel'] = env['ir.ui.view']._render_template(
                'website_sale.shop_product_images', {
                    'product': product_template,
                    'product_variant': candidate_product,
                    'website': website,
                }
            )

        if website.is_view_active('website_sale.product_tags'):
            combination_info['product_tags'] = env['ir.ui.view']._render_template(
                'website_sale.product_tags', {
                    'all_product_tags': candidate_product.all_product_tag_ids.filtered('visible_on_ecommerce')
                }
            )

        return combination_info
