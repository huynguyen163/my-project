# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Aura CRM Extendsion",
    "author": "FOSTECH",
    "website": "https://fostech.vn",
    "support": "info@fostech.vn",
    "license": "OPL-1",
    "category": "Extra Tools",
    "summary": "This module CRM customize for Aura ",
    "version": "15.0.0.2",
    "depends": [
            "crm", 'utm', 'sale'
    ],
    "application": True,
    "data": [
        'security/ir.model.access.csv',
        'wizard/message_wizard.xml',
        'data/campaign_type_data.xml',
        # Lead
        "security/import_lead_security.xml",
        "wizard/call_history_wizard_view.xml",
        "wizard/import_lead_wizard.xml",
        "wizard/assign_lead_to_saleperson_wizard_view.xml",
        # "views/crm_view.xml",
        # "views/utm_campaign_type_view.xml",
        "views/menu.xml",
    ],
    "external_dependencies": {
        "python": ["xlrd"],
    },

    "images": ["static/description/background.gif", ],
    "auto_install": False,
    "installable": True,
    "price": 80,
    "currency": "EUR"
}
