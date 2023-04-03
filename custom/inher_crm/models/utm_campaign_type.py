from odoo import fields, models

class UtmCampaignType(models.Model):
    _name = 'utm.campaign.type'
    _description = 'Utm Campaign Type'
    
    name = fields.Char(string= 'Name', required=True)

    
