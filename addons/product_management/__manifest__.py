# -*- coding: utf-8 -*-
{
    'name': 'Product Extension',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Manage Products, Suppliers, Inventory, and Transactions',
    'description': """
        A product management system for tracking products, suppliers, inventory, and transactions.
    """,
    'author': 'Edin Abdiu',
    'depends': ['base','sale_management', 'website_sale'],
    'data': [
        'views/product_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}