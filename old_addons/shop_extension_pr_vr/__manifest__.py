# -*- coding: utf-8 -*-
{
    'name': 'Shop Extension (Products Variant)',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Manage Products, Website and Shop Visibility',
    
    'description': """
        A module to manage products visibility in the shop.
    """,
    'author': 'Edin Abdiu',
    'depends': ['base','sale_management', 'website','website_sale'],
    'assets': {
        'website.assets_frontend': [
            'shop_extension_pr_vr/static/src/js/product_variant_patch.js',
        ],
    },
    'pre_init_hook': 'pre_init_hook',
    'data': [
        'views/product_view.xml',
        'views/website_view.xml',
        'views/filtered_variants_template.xml',
        'views/filtered_product_template.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}