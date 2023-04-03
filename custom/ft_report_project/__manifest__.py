{
  'name': 'Report Excel Project',
    'version': '15.0.1.0',
    'license': 'LGPL-3',
    'category': 'project',
    "sequence": 1,
    'complexity': "easy",
    'depends': [
        "project",
        "base",
    ],
    'data': [
    'security/ir.model.access.csv',
    'wizard/project_report_wizard_view.xml',
    # 'views/menu.xml',
    'report/report.xml',
    'report/project_report_pdf.xml',

    ],
}