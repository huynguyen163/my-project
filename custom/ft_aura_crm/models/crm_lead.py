# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2022 FOSTECH (<http://fostech.vn>).
#
##############################################################################
from odoo import models, fields, api, tools, _


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    def get_domain_mentor(self):
        employee_ids = self.env['hr.employee'].search([('job_title','=ilike','%Mentor')])
        return [('id','in',employee_ids.mapped('user_id').ids)]

    vat = fields.Char('VAT')
    tag_id = fields.Many2one('crm.tag', string='Tags')
    mentor_id = fields.Many2one('res.users', string = 'Mentor',domain=get_domain_mentor)
    history_ids = fields.One2many('crm.call.history','lead_id', string='Campaign')


    def click2call(self):
        pass

class CallHistory(models.Model):
    _name = 'crm.call.history'
    _description = 'CRM Call History'

    date = fields.Datetime(string='Call Date', default=lambda self: fields.datetime.now())
    user_id = fields.Many2one('res.users', string = 'Telesales')
    status = fields.Selection([('success','Success'),('busy','Busy'),('missed','Missed'),('no_answer','No Answer')],default="success", string= 'Call Status')
    descriptions = fields.Text("Description")
    lead_id = fields.Many2one('crm.lead','Opportunity')

class UTMCampaign(models.Model):
    _inherit= 'utm.campaign'

    stage = fields.Selection([('planing','Planing'),('completed','Completed'),('cancelled','Cancelled')], string='Status')

    campaign_type_id = fields.Many2one('utm.campaign.type' , string='Campaign Type')

class UtmCampaignType(models.Model):
    _name = 'utm.campaign.type'
    _description = 'Utm Campaign Type'
    
    name = fields.Char(string= 'Name', required=True)
    