# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ARMessageWizard(models.TransientModel):
    _name = "aura.message.wizard"
    _description = "Message wizard to display warnings, alert ,success messages"

    def get_default(self):
        if self.env.context.get("message", False):
            return self.env.context.get("message")
        return False

    def get_default_namefile(self):
        if self.env.context.get("namefile", False):
            return self.env.context.get("namefile")
        return False

    def get_datas(self):
        if self.env.context.get("file", False):
            return self.env.context.get("file")
        return False

    def get_datas_fail(self):
        if self.env.context.get("file_fail", False):
            return self.env.context.get("file_fail")
        return False

    def get_leads(self):
        if self.env.context.get("lead_ids", False):
            return self.env.context.get("lead_ids")
        return False

    name = fields.Text(string="Message", readonly=True, default=get_default)
    filename = fields.Char(
        string="File Name", readonly=True, default=get_default_namefile)
    datas = fields.Binary(string='Files', atttachment=False, default=get_datas)
    file_fail = fields.Binary(
        string='Files Fail', atttachment=False, default=get_datas_fail)
    lead_ids = fields.Many2many('crm.lead', string='Leads', default=get_leads)

    def export_file_report(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'web/content/?model=' + self._name + '&id=' + str(
                self.id) + '&field=datas&download=true&filename=' + self.filename,
        }

    def export_check_fail(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'web/content/?model=' + self._name + '&id=' + str(
                self.id) + '&field=file_fail&download=true&filename=' + "Data Fail",
        }

    def view_lead(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "crm.crm_lead_all_leads")
        action['view_mode'] = 'form'
        action['domain'] = [('id', 'in', self.lead_ids.ids)]
        return action


class ARMessageVerifyWizard(models.TransientModel):
    _name = "aura.message.verify.wizard"
    _description = "Message wizard to display warnings, alert ,success messages"

    def get_default(self):
        if self.env.context.get("message", False):
            return self.env.context.get("message")
        return False

    def get_datas(self):
        if self.env.context.get("file", False):
            return self.env.context.get("file")
        return False

    def get_default_namefile(self):
        if self.env.context.get("namefile", False):
            return self.env.context.get("namefile")
        return False

    def get_active_ids(self):
        active_ids = self.env.context.get("active_ids")
        wizard_close = self.env['import.lead.wizard'].browse(active_ids)
        if wizard_close:
            action = self.env["ir.actions.actions"]._for_xml_id(
                "ft_aura_crm.ft_import_lead_action")
            action['domain'] = [('id', '=', wizard_close.id)]
            action['context'] = {
                'default_file': self.env.context.get("master_file") or False}
            return action
        return True

    name = fields.Text(string="Message", readonly=True, default=get_default)
    datas = fields.Binary(
        string='Files', atttachment=False, default=get_datas)
    filename = fields.Char(
        string="File Name", readonly=True, default=get_default_namefile)

    def export_check_fail(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'web/content/?model=' + self._name + '&id=' + str(
                self.id) + '&field=datas&download=true&filename=' + self.filename,
        }

    def export_check_fail(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'web/content/?model=' + self._name + '&id=' + str(
                self.id) + '&field=datas&download=true&filename=' + self.filename,
        }
