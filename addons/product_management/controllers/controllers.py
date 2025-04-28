# -*- coding: utf-8 -*-
# from odoo import http


# class ProductManagement(http.Controller):
#     @http.route('/product_management/product_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_management/product_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_management.listing', {
#             'root': '/product_management/product_management',
#             'objects': http.request.env['product_management.product_management'].search([]),
#         })

#     @http.route('/product_management/product_management/objects/<model("product_management.product_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_management.object', {
#             'object': obj
#         })

