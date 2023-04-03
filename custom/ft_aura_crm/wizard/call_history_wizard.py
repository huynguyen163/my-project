from odoo import models, fields, api
from datetime import datetime

class CallHistoryWizard(models.TransientModel):
    _name =  'crm.call.history.wizard'
    _description = 'Utm Campaign Leads Wizard'

    user_id = fields.Many2one('res.users', string = 'Telesales', default=lambda self: self.env.user)
    call_status = fields.Selection([('success','Success'),('busy','Busy'),('missed','Missed'),('no_answer','No Answer')], string= 'Call Status', default='success')
    descriptions = fields.Text()
    

    
    def apply_call_history(self):
        self.ensure_one()
        active_id = self.env.context.get("lead_ids", False)
        if active_id:
            lead_id = self.env['crm.lead'].browse(active_id)
            vals = {
                'date': datetime.now(),
                'user_id':self.user_id.id,
                'call_status':self.call_status,
                'descriptions':self.descriptions,
                'lead_id': lead_id.id
            }
            self.env['crm.call.history'].sudo().create(vals)
        return True