{
'name': "CRM 1",
'version': '0.1.0',
'summary': '',
'sequence': 10,
'description': "",
'author': '',
'website': '',
'depends': ['base','crm', 'utm','sale','mail'],
'data':['security/group.xml',
        'security/ir.model.access.csv',
        'wizard/utm_campaign_leads_wizard_view.xml',
        'views/inher_crm_view.xml',
        'views/inher_menu_crm_view.xml',
        'views/utm_campaign_type_view.xml',
        'views/inher_utm_campaign_view.xml',
        'views/utm_campaign_leads_view.xml',
    ],
}