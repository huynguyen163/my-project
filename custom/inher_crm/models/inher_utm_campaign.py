from odoo import fields, models

class InheritTagIds(models.Model):
    _inherit= 'utm.campaign'


    stage = fields.Selection([('planing','Planing'),('completed','Completed'),('cancelled','Cancelled')], string='Status')

    campaign_type_id = fields.Many2one('utm.campaign.type' , string='Campaign Type')

    
    
    

    def action_campaign_leads():
        return