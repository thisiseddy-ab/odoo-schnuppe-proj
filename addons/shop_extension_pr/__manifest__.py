# -*- coding: utf-8 -*-
{
    'name': 'Shop Extension (Products)',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Manage Products, Website and Shop Visibility',
    
    'description': """
        A module to manage products visibility in the shop.
    """,
    'author': 'Edin Abdiu',
    'depends': ['base','sale_management', 'website','website_sale'],
    'data': [
        'views/product_tempalte_views.xml',
        'views/website_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}