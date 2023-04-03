# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _
from odoo.exceptions import UserError
import csv
import base64
import xlrd
from odoo.tools import ustr
import logging
import xlsxwriter
from io import BytesIO
import re


_logger = logging.getLogger(__name__)


class ImportLeadWizard(models.TransientModel):
    _name = "import.lead.wizard"
    _description = "Import Lead Wizard"

    method = fields.Selection([
        ('create', 'Create Lead'),
        ('write', 'Create or Update Lead')
    ], default="create", string="Method", required=True)

    lead_update_by = fields.Selection([
        ('phone', 'Phone'),
        ('email', 'Email'),
    ], default='phone', string="Lead Update By", required=True)

    file = fields.Binary(string="File", required=True)

    def validate_field_value(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        """ Validate field value, depending on field type and given value """
        self.ensure_one()

        try:
            checker = getattr(self, 'validate_field_' + field_ttype)
        except AttributeError:
            _logger.warning(
                field_ttype + ": This type of field has no validation method")
            return {}
        else:
            return checker(field_name, field_ttype, field_value, field_required, field_name_m2o)

    def validate_field_many2many(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            name_relational_model = self.env['crm.lead'].fields_get()[
                field_name]['relation']

            ids_list = []
            if field_value.strip() not in (None, ""):
                for x in field_value.split(','):
                    x = x.strip()
                    if x != '':
                        record = self.env[name_relational_model].sudo().search([
                            (field_name_m2o, '=', x)
                        ], limit=1)

                        if record:
                            ids_list.append(record.id)
                        else:
                            return {"error": " - " + x + " not found. "}
                            break

            return {field_name: [(6, 0, ids_list)]}

    def validate_field_many2one(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            name_relational_model = self.env['crm.lead'].fields_get()[
                field_name]['relation']
            record = self.env[name_relational_model].sudo().search([
                (field_name_m2o, '=', field_value)
            ], limit=1)
            return {field_name: record.id if record else False}

    def validate_field_text(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_integer(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_float(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_char(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_boolean(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        boolean_field_value = False
        if field_value.strip() == 'TRUE':
            boolean_field_value = True

        return {field_name: boolean_field_value}

    def validate_field_selection(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}

        # get selection field key and value.
        selection_key_value_list = self.env['crm.lead'].sudo(
        )._fields[field_name].selection
        if selection_key_value_list and field_value not in (None, ""):
            for tuple_item in selection_key_value_list:
                if tuple_item[1] == field_value:
                    return {field_name: tuple_item[0] or False}

            return {"error": " - " + field_name + " given value " + str(field_value) + " does not match for selection. "}

        # finaly return false
        if field_value in (None, ""):
            return {field_name: False}

        return {field_name: field_value or False}

    def dupplicate_file(self, vals):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        col = 0
        row = 0
        sheet.write(row, col, "TÊN CÔNG TY/ COMPANY NAME", bold)
        sheet.write(row, col+1, "MÃ SỐ THUẾ", bold)
        sheet.write(row, col+2, "ĐỊA CHỈ VP", bold)
        sheet.write(row, col+3, "NGƯỜI LIÊN HỆ CHÍNH", bold)
        sheet.write(row, col+4, "ĐIỆN THOẠI NGƯỜI LIÊN HỆ CHÍNH", bold)
        sheet.write(row, col+5, "EMAIL NGƯỜI LIÊN HỆ CHÍNH", bold)
        sheet.write(row, col+6, "CHỨC VỤ LIÊN HỆ CHÍNH", bold)
        sheet.write(row, col+7, "CHIẾN DỊCH KHÁCH HÀNG", bold)
        sheet.write(row, col+8, "NGUỒN KHÁCH HÀNG", bold)
        row += 1
        for val in vals:
            campaign = val.get("campaign_id") or False
            if campaign:
                campaign_id = self.env['utm.campaign'].browse(campaign)
            else:
                campaign_id = False
            source = val.get("source_id") or False
            if source:
                source_id = self.env['utm.source'].browse(source)
            else:
                source_id = False

            sheet.write(row, col, val.get("partner_name"))
            sheet.write(row, col+1, val.get("vat"))
            sheet.write(row, col+2, val.get("street2"))
            sheet.write(row, col+3, val.get("contact_name"))
            sheet.write(row, col+4, val.get("mobile"))
            sheet.write(row, col+5, val.get("email_from"))
            sheet.write(row, col+6, val.get("function"))
            sheet.write(row, col+7, campaign_id and campaign_id.name or "")
            sheet.write(row, col+8, source_id and source_id.name or "")
            row += 1

        workbook.close()
        output.seek(0)
        datas = base64.encodebytes(output.read())
        output.close()
        return datas

    def check_fail_file(self, vals):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        col = 0
        row = 0
        sheet.write(row, col, "TÊN CÔNG TY/ COMPANY NAME", bold)
        sheet.write(row, col+1, "MÃ SỐ THUẾ", bold)
        sheet.write(row, col+2, "ĐỊA CHỈ VP", bold)
        sheet.write(row, col+3, "NGƯỜI LIÊN HỆ CHÍNH", bold)
        sheet.write(row, col+4, "ĐIỆN THOẠI NGƯỜI LIÊN HỆ CHÍNH", bold)
        sheet.write(row, col+5, "EMAIL NGƯỜI LIÊN HỆ CHÍNH", bold)
        sheet.write(row, col+6, "CHỨC VỤ LIÊN HỆ CHÍNH", bold)
        sheet.write(row, col+7, "CHIẾN DỊCH KHÁCH HÀNG", bold)
        sheet.write(row, col+8, "NGUỒN KHÁCH HÀNG", bold)
        row += 1
        for val in vals:

            campaign = val.get("campaign_id") or False
            if campaign:
                campaign_id = self.env['utm.campaign'].browse(campaign)
            else:
                campaign_id = False
            source = val.get("source_id") or False
            if source:
                source_id = self.env['utm.source'].browse(source)
            else:
                source_id = False

            sheet.write(row, col, val.get("partner_name"))
            sheet.write(row, col+1, val.get("vat"))
            sheet.write(row, col+2, val.get("street2"))
            sheet.write(row, col+3, val.get("contact_name"))
            sheet.write(row, col+4, val.get("mobile"))
            sheet.write(row, col+5, val.get("email_from"))
            sheet.write(row, col+6, val.get("function"))
            sheet.write(row, col+7, campaign_id and campaign_id.name or "")
            sheet.write(row, col+8, source_id and source_id.name or "")
            row += 1

        workbook.close()
        output.seek(0)
        datas = base64.encodebytes(output.read())
        output.close()
        return datas

    def show_success_msg(self, counter, dup_counter, fail_count, file, file_fail, lead_ids, skipped_line_no):
        # open the new success message box
        view = self.env.ref('ft_aura_crm.aura_message_wizard')
        context = dict(self._context or {})
        dic_msg = ""
        if counter:
            dic_msg = str(counter) + " Records imported successfully"
        if dup_counter:
            dic_msg = str(counter) + " Records imported successfully"
            dic_msg += "\n" + str(dup_counter) + " Records dupplicate"
        if fail_count:
            dic_msg = str(counter) + " Records imported successfully"
            dic_msg += "\n" + str(dup_counter) + " Records dupplicate"
            dic_msg += "\n" + str(fail_count) + " Record is not valid"
        if skipped_line_no:
            dic_msg = dic_msg + "\nNote:"
        for k, v in skipped_line_no.items():
            dic_msg = dic_msg + "\nRow No " + k + " " + v + " "
        context['message'] = dic_msg
        context['file'] = file
        context['file_fail'] = file_fail
        context['namefile'] = "Dữ liệu trùng"
        context['lead_ids'] = lead_ids
        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'aura.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def show_success_verify(self, counter, file):
        view = self.env.ref('ft_aura_crm.aura_message_verify_wizard')
        context = dict(self._context or {})
        dic_msg = ""
        if counter:
            dic_msg = _("%s Record is not valid. " %
                        (counter))
        else:
            dic_msg = _("All records are valid - You can import file")
        # if skipped_line_no2:
        #     dic_msg = dic_msg + "\nNote:"
        context['namefile'] = "Danh sách data lỗi dữ liệu.xlsx"
        context['file'] = file
        context['master_file'] = self.file
        context['message'] = dic_msg
        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'aura.message.verify.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def verify_data(self):
        # perform import lead
        if self and self.file:
            for rec in self:
                counter = 0
                skipped_line_no2 = {}
                regex_email = r"^[a-zA-Z]+[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
                regex_phone = r"\b(((\+|)84)|(84)|0)(3|5|7|8|9)+([0-9]{8})\b"
                check_fail = []
                try:
                    wb = xlrd.open_workbook(
                        file_contents=base64.decodebytes(rec.file))
                    sheet = wb.sheet_by_index(0)

                    skip_header = True

                    for row in range(sheet.nrows):
                        if skip_header:
                            skip_header = False
                            continue
                        campaign_id = False
                        if sheet.cell(row, 7).value != '':
                            campaign = self.env['utm.campaign'].search(
                                [('name', '=', sheet.cell(row, 7).value)], limit=1)
                            if campaign:
                                campaign_id = campaign.id
                            else:
                                campaign = self.env['utm.campaign'].sudo().create({
                                    'name': sheet.cell(row, 7).value
                                })
                                campaign_id = campaign.id
                        source_id = False
                        if sheet.cell(row, 7).value != '':
                            source = self.env['utm.source'].search(
                                [('name', '=', sheet.cell(row, 8).value)], limit=1)
                            if source:
                                source_id = source.id
                            else:
                                source = self.env['utm.source'].sudo().create({
                                    'name': sheet.cell(row, 8).value
                                })
                                source_id = source.id
                        vals = {

                            'partner_name': sheet.cell(row, 0).value,
                            'vat': sheet.cell(row, 1).value,
                            'street2': sheet.cell(row, 2).value,
                            'contact_name': sheet.cell(row, 3).value,
                            'mobile': sheet.cell(row, 4).value,
                            'email_from': sheet.cell(row, 5).value,
                            'function': sheet.cell(row, 6).value,
                            'campaign_id': campaign_id,
                            'source_id': source_id,
                            'type': 'lead',
                        }

                        if sheet.cell(row, 4).value != '':
                            check_phone = re.fullmatch(
                                regex_phone, sheet.cell(row, 4).value)
                            if check_phone:
                                True
                            else:
                                counter = counter + 1
                                check_fail.append(vals)
                                continue
                        else:
                            counter = counter + 1
                            check_fail.append(vals)
                        if sheet.cell(row, 5).value != '':
                            check_email = re.fullmatch(
                                regex_email, sheet.cell(row, 5).value)
                            if check_email:
                                True
                            else:
                                counter = counter + 1
                                check_fail.append(vals)
                                continue
                        else:
                            counter = counter + 1
                            check_fail.append(vals)
                    if check_fail:
                        file = rec.check_fail_file(check_fail)
                    else:
                        file = False
                except Exception:
                    raise UserError(
                        _("Sorry, Your excel file does not match with our format"))

                res = rec.show_success_verify(
                    counter, file)
                return res

    def import_lead_apply(self):
        crm_lead_obj = self.env['crm.lead']
        ir_model_fields_obj = self.env['ir.model.fields']
        # perform import lead
        if self and self.file:
            for rec in self:
                counter = 0
                dup_counter = 0
                fail_count = 0
                skipped_line_no = {}
                # Add Two Dictionary
                dup_vals = []
                lead_ids = []
                fail_vals = []
                try:
                    wb = xlrd.open_workbook(
                        file_contents=base64.decodebytes(rec.file))
                    sheet = wb.sheet_by_index(0)

                    skip_header = True
                    for row in range(sheet.nrows):
                        if skip_header:
                            skip_header = False
                            counter = counter + 0
                            continue
                        campaign_id = False
                        if sheet.cell(row, 7).value != '':
                            campaign = self.env['utm.campaign'].search(
                                [('name', '=', sheet.cell(row, 7).value)], limit=1)
                            if campaign:
                                campaign_id = campaign.id
                            else:
                                campaign = self.env['utm.campaign'].sudo().create({
                                    'name': sheet.cell(row, 7).value
                                })
                                campaign_id = campaign.id
                        source_id = False
                        if sheet.cell(row, 7).value != '':
                            source = self.env['utm.source'].search(
                                [('name', '=', sheet.cell(row, 8).value)], limit=1)
                            if source:
                                source_id = source.id
                            else:
                                source = self.env['utm.source'].sudo().create({
                                    'name': sheet.cell(row, 8).value
                                })
                                source_id = source.id
                        regex_email = r"^[a-zA-Z]+[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
                        regex_phone = r"\b(((\+|)84)|(84)|0)(3|5|7|8|9)+([0-9]{8})\b"
                        check_phone = re.fullmatch(
                            regex_phone, sheet.cell(row, 4).value)
                        check_email = re.fullmatch(
                            regex_email, sheet.cell(row, 5).value)
                        try:
                            vals = {
                                'name': 'New',
                                'partner_name': sheet.cell(row, 0).value,
                                'vat': sheet.cell(row, 1).value,
                                'street2': sheet.cell(row, 2).value,
                                'contact_name': sheet.cell(row, 3).value,
                                'mobile': sheet.cell(row, 4).value,
                                'email_from': sheet.cell(row, 5).value,
                                'function': sheet.cell(row, 6).value,
                                'campaign_id': campaign_id,
                                'source_id': source_id,
                                'type': 'lead',
                                'user_id': ''
                            }

                            if self.method == 'create':
                                if check_email and check_phone and sheet.cell(row, 4).value != '' and sheet.cell(row, 5).value != '':
                                    search_lead = crm_lead_obj.search(
                                        ['|', ('mobile', '=', sheet.cell(row, 4).value), ('email_from', '=', sheet.cell(row, 5).value)], limit=1)

                                    if search_lead:
                                        dup_vals.append(vals)
                                        dup_counter += 1
                                        continue
                                    else:
                                        lead_id = crm_lead_obj.create(vals)
                                        lead_ids.append(lead_id.id)
                                        counter = counter + 1
                                else:
                                    fail_count += 1
                                    fail_vals.append(vals)
                            elif self.method == 'write' and self.lead_update_by == 'phone':
                                if check_email and check_phone and sheet.cell(row, 4).value != '' and sheet.cell(row, 5).value != '':
                                    search_lead = crm_lead_obj.search(
                                        [('mobile', '=', sheet.cell(row, 4).value)], limit=1)
                                    if search_lead:
                                        created_lead = search_lead
                                        search_lead.write(vals)
                                        counter = counter + 1
                                    else:
                                        created_lead = crm_lead_obj.create(
                                            vals)
                                        lead_ids.append(created_lead.id)
                                        counter = counter + 1
                                else:
                                    fail_count += 1
                                    fail_vals.append(vals)

                            elif self.method == 'write' and self.lead_update_by == 'email':
                                if check_email and check_phone and sheet.cell(row, 4).value != '' and sheet.cell(row, 5).value != '':
                                    search_lead = crm_lead_obj.search(
                                        [('email_from', '=', sheet.cell(row, 5).value)], limit=1)
                                    if search_lead:
                                        created_lead = search_lead
                                        search_lead.write(vals)
                                        counter = counter + 1
                                    else:
                                        created_lead = crm_lead_obj.create(
                                            vals)
                                        lead_ids.append(created_lead.id)
                                        counter = counter + 1
                                else:
                                    fail_count += 1
                                    fail_vals.append(vals)
                        except Exception as e:
                            skipped_line_no[str(
                                counter)] = " - Value is not valid " + ustr(e)
                            counter = counter + 1
                            continue
                    if dup_vals:
                        file = rec.dupplicate_file(dup_vals)
                    else:
                        file = False
                    if fail_vals:
                        file_fail = rec.dupplicate_file(fail_vals)
                    else:
                        file_fail = False
                except Exception:
                    raise UserError(
                        _("Sorry, Your excel file does not match with our format"))

                res = rec.show_success_msg(
                    counter, dup_counter, fail_count, file, file_fail, lead_ids, skipped_line_no)
                return res
        # sale person
