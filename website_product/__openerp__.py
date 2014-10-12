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
    'depends': ['website', 'product'],
    'data': [
        'data/website_product_data.xml',
        'views/website_product.xml',
        'security/ir.model.access.csv',
        'security/website_product.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
