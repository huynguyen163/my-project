from odoo import models, fields, api

class UtmCampaignLeadsWizard(models.TransientModel):
    _name =  'utm.campaign.leads.wizard'
    _description = 'Utm Campaign Leads Wizard'

    call_date = fields.Datetime(string= 'Call Date', default=lambda self: fields.datetime.now())
    telesales_staff = fields.Many2one('res.users', string = 'Telesales Staff', default=lambda self: self.env.user)
    call_status = fields.Selection([('success','Success'),('busy','Busy'),('missed','Missed')], string= 'Call Status', default='success')
    call_content = fields.Html()
    lead_id = fields.Many2one('crm.lead', string='Opportunity' ,default=lambda self: self.env['crm.lead'].search([]) )
    

    
    def multi_update(self): 
        vals = {
            'call_date':self.call_date,
            'telesales_staff':self.telesales_staff.id,
            'call_status':self.call_status,
            'call_content':self.call_content,
            'lead_id': self.lead_id.id
        } 
           
        create_history_call = self.env["utm.campaign.lead"].create(vals)
    

  