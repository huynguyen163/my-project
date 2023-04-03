from odoo import models, fields, api

class ProjectReportWizard(models.TransientModel):
    _name =  'project.report.wizard'
    _description = 'Project Report Wizard'

    start_date = fields.Date(string='Start Date', required= True)
    end_date = fields.Date(string='End Date', required= True)
    user_id = fields.Many2one('res.users', string='User', required= True, default=lambda self: self.env.user)
    stage = fields.Many2one('project.project.stage', string='Stage', required= True, default=lambda self: self.env['project.project.stage'].search([]))
    project = fields.Many2one('project.project', string='Project', required= True, default=lambda self: self.env['project.project'].search([]))
    
    def action_print_report_excel(self):
        domain=[]
        user_id = self.user_id
        if user_id:
            domain += [('portal_user_names','=',user_id.name)]
        start_date = self.start_date
        if start_date:
            domain += [('date_assign','>=',start_date)]
        end_date = self.end_date 
        if end_date :
            domain += [('date_deadline','<=',end_date)]
        stage = self.stage
        if stage:
            domain += [('stage_id', '=',stage.id)]
        project = self.project
        if project:
            domain += [('project_id', '=', project.id)]
            
        projects= self.env['project.task'].search_read(domain)
          
        data = {
            'projects': projects,
            'user_id': self.user_id.name,
            'start_date' : self.start_date,
            'end_date' : self.end_date,
            'stage' : self.stage.name,
            'project' : self.project.name,
            'form_data':self.read()[0],
        }
        return self.env.ref('ft_report_project.report_project_xls').report_action(self, data=data)








    def action_print_report_pdf(self):
        domain=[]
        user_id = self.user_id
        if user_id:
            domain += [('portal_user_names','=',user_id.name)]
        start_date = self.start_date
        if start_date:
            domain += [('date_assign','>=',start_date)]
        end_date = self.end_date 
        if end_date :
            domain += [('date_deadline','<=',end_date)]
        stage = self.stage
        if stage:
            domain += [('stage_id', '=',stage.id)]
        project = self.project
        if project:
            domain += [('project_id', '=', project.id)]
            
        projects= self.env['project.task'].search_read(domain)
          
        data = {
            'projects': projects,
            'user_id': self.user_id.name,
            'start_date' : self.start_date,
            'end_date' : self.end_date,
            'stage' : self.stage.name,
            'project' : self.project.name,
            'form_data':self.read()[0],
        }
        return self.env.ref('ft_report_project.report_project_pdf').report_action(self, data=data)
