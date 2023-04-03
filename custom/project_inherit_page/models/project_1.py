from odoo import fields, models

class ProjectTask1(models.Model):
    _inherit = 'project.task'

    name_sheet = fields.Char(string= 'Name')