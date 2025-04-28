# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class ShopController(http.Controller):

    @http.route('/shop', type='http', auth="public", website=True)
    def shop(self, **kwargs):
        shop = request.env['website'].get_current_website() 
        shop_type = shop.shop_type  

        print("Shop Type")
        # Filter products based on the shop ype of the shop
        if shop_type == 'b2b':
            # For B2B, filter products accordingly
            products = request.env['product.product'].search([('buisness_type', '=', 'b2b'), ('shop_visibility', '=', True)])
        else:
            # For B2C, filter products accordingly
            products = request.env['product.product'].search([('buisness_type', '=', 'b2c'), ('shop_visibility', '=', True)])

        print("Im Here")
        # Render the filtered products using the default website_sale template
        return request.render('website_sale.products', {
            'products': products,
            'page_name': 'shop',
        })