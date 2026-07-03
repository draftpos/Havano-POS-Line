{
    'name': 'POS License Management',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Generate and monitor licenses for Desktop POS',
    'description': """
        This module manages POS licenses, generating keys based on Machine IDs and monitoring their expiry.
    """,
    'author': 'Havano',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/license_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pos_license_management/static/src/dashboard/dashboard.js',
            'pos_license_management/static/src/dashboard/dashboard.xml',
            'pos_license_management/static/src/dashboard/dashboard.scss',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
