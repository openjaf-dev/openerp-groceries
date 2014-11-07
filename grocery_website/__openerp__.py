{
    'name': 'CRUD Product',
    'category': 'Website',
    'summary': 'Present Products',
    'version': '1.0',
    'description': """
Our Products
=============

        """,
    'author': 'OpenJAF',
    'depends': ['website', 'product', 'auth_signup'],
    'data': [
        'data/website_product_data.xml',
        'views/website_product.xml',
        'views/website_pos.xml',
        'views/website_partner.xml',
        'security/ir.model.access.csv',
        'security/website_product.xml',
    ],
    'js': [
        'static/src/js/widgets.js'
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
