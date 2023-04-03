from odoo import fields, models

class ProjectTask2(models.Model):
    _inherit = 'project.task'

    start_date = fields.Date(string= 'Start Date')
   