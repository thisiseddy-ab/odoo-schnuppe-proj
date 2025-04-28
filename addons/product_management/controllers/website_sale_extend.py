
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request
from odoo.osv import expression

'''
## Test Log##
import logging
_logger = logging.getLogger(__name__)
'''

class WebsiteSaleExtend(WebsiteSale):

    @http.route('/b2c/shop', type='http', auth="public", website=True)
    def b2c(self, page=0, category=None, search='', **post):
        """ Override the shop route to add a custom filter for B2C """
        
        request.update_context(shop_type='b2c')
        return super(WebsiteSaleExtend, self).shop(page=page, category=category, search=search, **post)

    @http.route('/b2b/shop', type='http', auth="public", website=True)
    def b2b(self, page=0, category=None, search='', **post):
        """ Override the shop route to add a custom filter for B2B """
        
        request.update_context(shop_type='b2b')
        return super(WebsiteSaleExtend, self).shop(page=page, category=category, search=search, **post)

    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        """ Override Odoo's internal product search logic to filter by buisness_type """

        # Standard behavior first
        fuzzy_search_term, product_count, search_product = super()._shop_lookup_products(attrib_set, options, post, search, website)

        # Now apply your custom filter
        shop_type = request.context.get('shop_type')
        if shop_type:
            search_product = search_product.filtered(lambda p: p.shop_type == shop_type and p.shop_visibility)

        return fuzzy_search_term, len(search_product), search_product