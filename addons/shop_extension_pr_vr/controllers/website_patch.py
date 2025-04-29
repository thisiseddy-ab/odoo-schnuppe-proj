from odoo import http
from odoo.addons.website.controllers.main import Website as WebsiteMain

class WebsiteCustomRedirect(WebsiteMain):

    @http.route('/', auth="public", website=True, sitemap=True)
    def index(self, **kw):
        website = http.request.env['website'].get_current_website()

        if website and website.shop_type:
            shop_type = website.shop_type
            path = http.request.httprequest.path

            if not path.startswith(f'/{shop_type}'):
                # Redirect to /b2b/ or /b2c/ homepage
                new_path = f'/{shop_type}{path}'

                query_string = http.request.httprequest.query_string.decode()
                if query_string:
                    new_path += '?' + query_string

                return http.request.redirect(new_path, code=301)

        # fallback to normal homepage behavior
        return super().index(**kw)
