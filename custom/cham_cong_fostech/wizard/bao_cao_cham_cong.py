# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import calendar
import datetime
from datetime import datetime, date, timedelta
from odoo.tools.misc import get_lang, babel_locale_parse
from calendar import monthrange


class ChamCongFostechReportWizard(models.TransientModel):
    _name = "cham.cong.fostech.report.wizard"
    _description = "Chấm Công"

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    def action_print_report(self):
        print("Excel")

        self.ensure_one()
        year = self.start_date.year
        month = self.start_date.month
        days = monthrange(year, month)[1]
        date_list = []
        for day in range(1, days+1):
            a = date(year, month, day)
            if a.weekday() < 5:
                date_list.append(str(a))

        lst = []
        # lấy tất cả các nhân viên trên hệ thống (active = True)
        employees = self.env['hr.employee'].search(
            [('active', '=', True), ])

        for employee in employees:
            vals = {}
            phep = 0
            khong_luong = 0
            nua_ngay = 0
            tru_nua = 0
            total_phep = employee.allocation_count
            nghi_le = 0
            strs = ""

            # Lấy tất cả các ngày công của nhân viên
            attendances = self.env['hr.attendance'].search(
                [('check_in', '>=', self.start_date), ('check_in', '<=', self.end_date), ('check_out', '!=', False), ('employee_id', '=', employee.id)])

            cong_ngay = attendances and len(attendances) or 0
            vals = {
                'ma_nhan_vien': employee.barcode,
                'nhan_vien': employee.name,
                'bo_phan': employee.department_id.name,
                'nghi_le': nghi_le,
                'cong_ngay': cong_ngay,
            }
            # Lấy ngày nghỉ phép trong tháng
            leaves = self.env['hr.leave'].search([('date_from', '>=', self.start_date), (
                'date_to', '<=', self.end_date), ('state', '=', 'validate')])

            for leave in leaves:
                print(leave.holiday_status_id.time_type)
                #       ',,,,,,,,,,,,,,,,,,,,,,,,,')
                # kiểm tra nhân viên nào làm đề xuất nghỉ phép thì ghi nhận
                if employee.id in leave.employee_ids.ids:
                    # kiểm tra ngày nghỉ phép có lương
                    if leave.holiday_status_id.time_type == 'leave':
                        if leave.holiday_status_id.ids == [1]:
                            if leave.request_unit_half:
                                # phep += 0.5
                                nua_ngay += 0.5
                                strs += " Ngày %s nghỉ phép có lương 0,5 ngày \n" % (
                                    leave.request_date_from)

                            else:
                                phep += 1
                                strs += " Ngày %s nghỉ phép có lương 1 ngày \n" % (
                                    leave.request_date_from)
                        if leave.holiday_status_id.ids == [4]:
                            if leave.request_unit_half:
                                # khong_luong += 0.5
                                tru_nua += 0.5
                                strs += " Ngày %s nghỉ không lương 0,5 ngày \n" % (
                                    leave.request_date_from)

                            else:
                                khong_luong += 1
                                strs += " Ngày %s nghỉ không lương 1 ngày \n" % (
                                    leave.request_date_from)
                    else:()
                        # không lương
                        # if leave.request_unit_half:
                        #     khong_luong += 0.5
                        #     tru_nua += 1
                        #     strs += " Ngày %s nghỉ không lương 0,5 ngày \n" % (
                        #         leave.request_date_from)
                        # else:
                        #     khong_luong += 1
                        #     strs += " Ngày %s nghỉ không lương 1 ngày \n" % (
                        #         leave.request_date_from)
            vals.update({
                'khong_luong': khong_luong,
                'so_phep': phep,
                'ghi_chu': strs,
                'tru_nua': tru_nua,
                'nua_ngay': nua_ngay,
                'ngay_cong_tinh_luong': cong_ngay + phep + nghi_le - tru_nua,
                # lay số phép của nhân viên được phân bổ
                'so_phep_cua_nhan_vien': total_phep,
                'so_phep_con_lai_nhan_vien': total_phep - phep - nua_ngay,
                'ky_xac_nhan': ""
            })

            lst.append(vals)
            
        data = {
            'lst': lst
        }
        report = self.env.ref(
            'cham_cong_fostech.report_xlsx_cham_cong_action').report_action(None, data=data)
        return report
