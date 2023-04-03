from odoo import fields, models

class UtmCampaignLead(models.Model):
    _name = 'utm.campaign.lead'
    _description = 'Utm Campaign Lead'

    call_date = fields.Datetime(string= 'Call Date', default=lambda self: fields.datetime.now())
    telesales_staff = fields.Many2one('res.users', string = 'Telesales Staff', default=lambda self: self.env.user)
    call_status = fields.Selection([('success','Success'),('busy','Busy'),('missed','Missed')], string= 'Call Status', default='success')
    call_content = fields.Html()
    lead_id = fields.Many2one('crm.lead', string='Opportunity' ,default=lambda self: self.env['crm.lead'].search([]) )

