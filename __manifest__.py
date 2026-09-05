{
    'name': 'POS License Management',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Generate and monitor licenses for Desktop POS',
    'description': """
        This module manages POS licenses, generating keys based on Machine IDs and monitoring their expiry directly from Settings.
    """,
    'author': 'Havano',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/license_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
