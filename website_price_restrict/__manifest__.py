# -*- coding: utf-8 -*-
{
    'name': "Website price hide for non logged in user",
    "version": "1.0.0",
    'category': 'Website',
    'summary': """Website price hide for non logged in user""",
    'description': """For logged-in users, the shop page will display the product price. 
        Additionally, logged-in users will be able to view the price, quantity, and access the "Add To Cart" button. 
        However, for non logged in users, these features will remain hidden.""",
    'author': 'Flyers Friday',
    'images': ['static/description/banner.jpg'],
    'depends': ['website_sale'],
    'data': [
        'views/product_page_template.xml',
        'views/shop_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_price_restrict/static/src/scss/product_detail.scss'
        ]
    },
    'license': 'AGPL-3',
    'installable': True,
}
