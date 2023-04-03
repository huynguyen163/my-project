from odoo import fields, models

class InheritTagIds(models.Model):
    _inherit= 'crm.lead'
 
    tag_ids_2 = fields.Many2one('crm.tag', string = 'Tags')


    campaign_ids = fields.One2many('utm.campaign.lead','lead_id', string='Campaign')
    
    call_date = fields.Datetime(string= 'Call Date')
    telesales_staff = fields.Many2one('res.users', string = 'Telesales Staff')
    call_status = fields.Selection([('success','Success'),('busy','Busy'),('missed','Missed')], string= 'Call Status')
    call_content = fields.Html()


    
