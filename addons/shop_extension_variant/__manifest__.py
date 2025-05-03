# -*- coding: utf-8 -*-
{
    'name': 'Shop Extension (Variant)',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Manage Products, Website and Shop Visibility',
    
    'description': """
        A module to manage products visibility in the shop.
    """,
    'author': 'Edin Abdiu',
    'depends': ['base','sale_management', 'website','website_sale'],
    'assets': {
    },
    'data': [
        'views/product_view.xml',
        'views/website_view.xml',
        'views/variant_template.xml',
        'views/product_template.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}