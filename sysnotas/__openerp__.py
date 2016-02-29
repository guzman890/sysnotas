# -*- coding: utf-8 -*-
{
    'name': "sistemas de matriculas",

    'summary': """
        sistemas de matriculas de ubuntu""",

    'description': """
        sistemas de matriculas
    """,

    'author': "mee",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/main.xml',
        'views/curso.xml',
        'views/alumno.xml',
        'views/matricula.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
