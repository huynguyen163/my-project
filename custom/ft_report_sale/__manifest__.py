# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
  'name': 'Report Excel Sale',
    'version': '15.0.1.0',
    'license': 'LGPL-3',
    'category': 'sale',
    "sequence": 1,
    'complexity': "easy",
    'depends': [
        "sale",
        "base",
    ],
    'data': [
        "security/ir.model.access.csv",
        "wizard/export_excel.xml",
        "views/menu.xml",


    ],
}