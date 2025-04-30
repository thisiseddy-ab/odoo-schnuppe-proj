
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
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

    @http.route(['/shop', '/shop/<path:anything>'], type='http', auth="public", website=True)
    def redirect_shop(self, anything=None, **kwargs):
        """Redirect everything starting with /shop to /<shop_type>/shop/..."""
        website = http.request.env['website'].get_current_website()
        shop_type = website.shop_type

        if not shop_type:
            raise NotFound()

        original_path = http.request.httprequest.path  # e.g., /shop/category/test
        if not original_path.startswith('/shop'):
            raise NotFound()

        # Redirect to /b2b/shop/... or /b2c/shop/...
        new_path = f"/{shop_type}" + original_path
        return http.request.redirect(new_path, code=301)
    
    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_product = super()._shop_lookup_products(attrib_set, options, post, search, website)

        website = http.request.env['website'].get_current_website()
        shop_type = website.shop_type

        if shop_type:
            filtered_products = []
            for template in search_product:
                # Check if any variant matches
                variants = template.product_variant_ids.filtered(lambda p: p.shop_visibility in [shop_type, 'both'])
                if variants:
                    filtered_products.append(template)
            
            search_product = http.request.env['product.template'].browse([p.id for p in filtered_products])

        return fuzzy_search_term, len(search_product), search_product
    
    '''
    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_products, readonly=True)
    def product(self, product, category='', search='', **kwargs):
        if not http.request.website.has_ecommerce_access():
            return http.request.redirect('/web/login')

        website = http.request.env['website'].get_current_website()
        shop_type = website.shop_type

        # Filter variants (don't modify original product)
        visible_variants = product.product_variant_ids.filtered(
            lambda p: p.shop_visibility in [shop_type, 'both']
        )

        # Optional: redirect if no visible variants
        if not visible_variants:
            return http.request.redirect('/shop')

        # Create a temporary in-memory copy of the product with filtered variants
        product_with_filtered_variants = product.with_context(
            override_visible_variants=visible_variants.ids
        )

        # Inside _prepare_product_values you will check this context
        product_values = super()._prepare_product_values(product_with_filtered_variants, category, search, **kwargs)

        return http.request.render("website_sale.product", product_values)
    
    '''
    '''
    
    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=True)
    def product(self, product, category='', search='', **kwargs):
        if not http.request.website.has_ecommerce_access():
            return http.request.redirect('/web/login')

        product_values = self._prepare_product_values(product, category, search, **kwargs)
        return http.request.render("website_sale.product", product_values)

    def _prepare_product_values(self, product, category, search, **kwargs):
        product = product.with_context(website_shop_filter=True)

        values = super()._prepare_product_values(product, category, search, **kwargs)

        # Overwrite both product references
        values['product'] = product
        values['main_object'] = product

        # Inject filtered attribute lines if you hide some variants
        values['visible_attribute_lines'] = product._get_filtered_attribute_lines_for_website()

        return values
    '''
