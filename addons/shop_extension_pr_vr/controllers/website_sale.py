
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound


#'''
## Test Log##
import logging
_logger = logging.getLogger(__name__)
#'''

class WebsiteSaleExtend(WebsiteSale):

    @http.route(['/b2c/shop', '/b2c/shop/page/<int:page>', 
                 '/b2c/shop/category/<model("product.public.category"):category>', 
                 '/b2c/shop/category/<model("product.public.category"):category>/page/<int:page>'],
                type='http', auth="public", website=True)
    def b2c(self, page=0, category=None, search='', **post):
        return super().shop(page=page, category=category, search=search, **post)

    @http.route(['/b2b/shop', '/b2b/shop/page/<int:page>', 
                 '/b2b/shop/category/<model("product.public.category"):category>', 
                 '/b2b/shop/category/<model("product.public.category"):category>/page/<int:page>'],
                type='http', auth="public", website=True)
    def b2b(self, page=0, category=None, search='', **post):
        return super().shop(page=page, category=category, search=search, **post)

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def redirect_shop(self, page=0, category=None, **kwargs):
        """Redirect /shop and all subpaths to /b2c/shop/... or /b2b/shop/..."""

        website = request.env['website'].get_current_website()
        shop_type = website.shop_type

        if not shop_type:
            raise NotFound()

        original_path = request.httprequest.path  # /shop/category/xyz
        if not original_path.startswith('/shop'):
            raise NotFound()

        new_path = f"/{shop_type}" + original_path
        return request.redirect(new_path, code=301)

    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_product = super()._shop_lookup_products(attrib_set, options, post, search, website)

        website = request.env['website'].get_current_website()
        shop_type = website.shop_type

        if shop_type:
            filtered_products = []
            for template in search_product:
                # Check if any variant matches
                variants = template.product_variant_ids.filtered(lambda p: p.shop_visibility in [shop_type, 'both'])
                if variants:
                    filtered_products.append(template)
            
            search_product = request.env['product.template'].browse([p.id for p in filtered_products])

        return fuzzy_search_term, len(search_product), search_product
        
    '''
    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        website = request.env['website'].get_current_website()
        shop_type = website.shop_type

        # Call default method first
        values = super()._prepare_product_values(product, category, search, **kwargs)

        # Now safely patch the result (in-memory)
        display_product = values['product'].with_prefetch(values['product']._prefetch_ids)

        # Filter variants
        filtered_variants = display_product.product_variant_ids.filtered(
            lambda v: v.shop_visibility in [shop_type, 'both']
        )

        # Filter attribute lines
        allowed_value_ids = filtered_variants.mapped(
            'product_template_attribute_value_ids.product_attribute_value_id.id'
        )
        filtered_attribute_lines = display_product.attribute_line_ids.filtered(
            lambda line: any(val.id in allowed_value_ids for val in line.value_ids)
        )

        # Patch in-memory (important: after super())
        object.__setattr__(display_product, 'product_variant_ids', filtered_variants)
        object.__setattr__(display_product, 'attribute_line_ids', filtered_attribute_lines)

        # Replace in the values dict
        values['product'] = display_product
        values['main_object'] = display_product  # also used in templates
        _logger.info("I'm HERE")


        return request.render("website_sale.product", values)
    '''
