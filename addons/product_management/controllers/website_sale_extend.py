
from addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

class WebsiteSaleExtend(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values, **post):
        domain = super()._get_search_domain(search, category, attrib_values, **post)

        website = request.env['website'].get_current_website()
        shop_type = website.shop_type
        
        if shop_type:
            domain += [
                ('shop_visibility', '=', True),
                ('shop_type', '=', shop_type),
            ]
        else:
            # Optional: fallback if no shop_type is set
            domain += [('shop_visibility', '=', True)]

        return domain