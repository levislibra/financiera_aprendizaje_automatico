# -*- coding: utf-8 -*-
{
    'name': "Financiera Aprendizaje Automatico",

    'summary': """
        Modulo sobre inteligencia de datos y aprendizaje automatico.""",

    'description': """
        Modulo sobre inteligencia de datos y aprendizaje automatico.
    """,

    'author': "Librasoft",
    'website': "https://libra-soft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'finance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'financiera_prestamos'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/aa_config.xml',
				'views/extends_res_company.xml',
				'views/extends_res_partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}