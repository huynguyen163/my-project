# -*- coding: utf-8 -*-
import base64
from datetime import date, time, datetime
from logging import Logger
import tempfile
from odoo import models, fields, _
from odoo.exceptions import UserError
try:
    import xlsxwriter
except ImportError:
    Logger.warning("Cannot import xlsxwriter")
    xlsxwriter = False


class WizardTrainerEmployee(models.TransientModel):
    _name = 'sale.report.wizard'

    partner_id = fields.Many2one('res.partner', "Customer")
    user_id = fields.Many2one('res.users', "Sale")
    from_date = fields.Date('From date')
    date_to = fields.Date('To date')

    def generate_xlsx_report(self):
        partner_id = self.partner_id and self.partner_id or False
        user_sale_id = self.user_id and self.user_id or False
        datefrom = self.from_date and self.from_date or False
        dateto = self.date_to and self.date_to or False
        # Khai báo file excel--------------------------------------------
        if not xlsxwriter:
            raise UserError(
                _("The Python library xlsxwriter is installed. Contact your system administrator"))

        file_name = u"Báo cáo doanh thu.xlsx"
        file_path = tempfile.mktemp(suffix='.xlsx')
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet("Báo cáo doanh thu")
        # Header---------------------------------------------------------
        main_header_style = workbook.add_format({
            'bold': True,
            'font_size': 11,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#92D050',
            'border_color': 'black',
        })
        main_cell_style_dict = {
            'font_size': 11,
            'border': 1,
            'border_color': 'gray',
        }
        user_style = {
            'color': "red",
            'bold': True,
        }

        column_keys = [
            {"key": "A", "label": _(""), "width": 4},
            {"key": "B", "label": _(""), "width": 35},
            {"key": "C", "label": _("DOANH THU"), "width": 20},
            {"key": "D", "label": _("HOA HỒNG"), "width": 20},
            {"key": "E", "label": _("ST CÒN LẠI"), "width": 20},
        ]
        # Data------------------------------------------------------------
        result, length, data_user, data_total = self.data_export(
            datefrom, dateto, user_sale_id, partner_id)
        # Render data-----------------------------------------------------
        for ccolumn in column_keys:
            ckey = ccolumn.get("key")
            # set columns
            worksheet.set_column('{c}:{c}'.format(
                c=ckey), ccolumn.get("width"))
            # set header row
            worksheet.write("{}3".format(ckey), ccolumn.get(
                "label"), main_header_style)

            for row_number in range(4, length+1):
                cell_number = "{}{}".format(ckey, row_number)
                cell_value_dict = result.get(cell_number)
                cell_value = ""
                # cell_level = 0
                cell_style = main_cell_style_dict.copy()
                if cell_value_dict:
                    cell_value = cell_value_dict.get("value")
                    cell_style.update(cell_value_dict.get("style"))
                cell_style = workbook.add_format(cell_style)
                worksheet.write(
                    cell_number,
                    cell_value,
                    cell_style,
                )
        worksheet.merge_range('A1:E2', "BÁO CÁO DOANH THU",
                              workbook.add_format({'align': 'center', 'bold': True, 'font_size': 20}))
        worksheet.merge_range('A3:B3', "DIỄN GIẢI", main_header_style)
        for data in data_user:
            worksheet.merge_range('A{}:B{}'.format(data.get("index"), data.get(
                "index")), data.get("data"), workbook.add_format(user_style))
        # Footer
        footer = [
            {"key": "B{}".format(length+3), "label": _("Người lập"),
             "style": {'align': 'center', 'bold': True}},
            {"key": "C{}".format(length+3), "label": _("Kế toán trưởng"),
             "style": {'align': 'center', 'bold': True}},
            {"key": "D{}".format(length+3), "label": _("GĐ.Kinh doanh"),
             "style": {'align': 'center', 'bold': True}},
            {"key": "E{}".format(length+3), "label": _("Giám đốc"),
             "style": {'align': 'center', 'bold': True}},
            {"key": "B{}".format(
                length+4), "label": _("(Ký, họ tên)"), "style": {'align': 'center', }},
            {"key": "C{}".format(
                length+4), "label": _("(Ký, họ tên)"), "style": {'align': 'center', }},
            {"key": "D{}".format(
                length+4), "label": _("(Ký, họ tên)"), "style": {'align': 'center', }},
            {"key": "E{}".format(
                length+4), "label": _("(Ký, họ tên)"), "style": {'align': 'center', }},
            {"key": "E{}".format(length+2), "label": _("Ngày....tháng....năm...."),
             "style": {'align': 'center', 'italic': True}},
        ]

        worksheet.write("B{}".format(length), "Tổng cộng : ",
                        workbook.add_format({'align': 'right', 'bold': True, 'border': 1, "num_format": "#,##0.00"}))
        worksheet.write("C{}".format(length), data_total.get("price"),
                        workbook.add_format({'align': 'right', 'bold': True, 'border': 1, "num_format": "#,##0.00"}))
        worksheet.write("D{}".format(length),  data_total.get("discount"),
                        workbook.add_format({'align': 'right', 'bold': True, 'border': 1, "num_format": "#,##0.00"}))
        worksheet.write("E{}".format(length), data_total.get("total"),
                        workbook.add_format({'align': 'right', 'bold': True, 'border': 1, "num_format": "#,##0.00"}))
        for f in footer:
            worksheet.write(
                f.get("key"),
                f.get("label"),
                workbook.add_format(f.get("style"))
            )

        workbook.close()
        # Xuất excel--------------------------------------
        with open(file_path, 'rb') as r:
            xls_file = base64.b64encode(r.read())
        att_vals = {
            'name': file_name,
            'type': 'binary',
            'datas': xls_file,
        }
        attachment_id = self.env['ir.attachment'].create(att_vals)
        self.env.cr.commit()
        action = {
            'type': 'ir.actions.act_url',
            'url': '/web/content/{}?download=true'.format(attachment_id.id, ),
            'target': 'self',
        }
        return action

    def data_export(self, from_date, to_date, sale_user, partner_id):

        data = self.get_data_from_sql(
            from_date, to_date, sale_user, partner_id)
        result = {}
        user_result = []
        # -----------------------------
        price_all = 0
        discount_all = 0
        total_all = 0
        # Row-------------------------
        row = 6
        row_category = 5
        row_user_id = 4
        # cate data------------------
        cate_price = 0
        cate_discount = 0
        cate_total = 0
        # user data------------------
        user_price = 0
        user_discount = 0
        user_total = 0
        # Style row-------------------

        default_style = {
            "color": "black"
        }
        default_style_money = {
            "num_format": "#,##0.00"
        }
        user_style_money = {
            'color': "red",
            'bold': True,
            "num_format": "#,##0.00"
        }
        category_style = {
            'bold': True,
        }
        user_style = {
            'color': "red",
            'bold': True,
        }
        line_index = 1
        cate_index = 1
        user = data[0][0]
        result.update({
            "C{}".format(row_user_id): {"value": 0, "style": user_style_money},
            "D{}".format(row_user_id): {"value": 0, "style": user_style_money},
            "E{}".format(row_user_id): {"value": 0, "style": user_style_money},
        })
        user_result.append({"index": row_user_id, "data": data[0][1]})
        cate = data[0][2]
        result.update({
            "A{}".format(row_category): {"value": cate_index, "style": category_style},
            "B{}".format(row_category): {"value": data[0][3], "style": category_style},
            "C{}".format(row_category): {"value": 0, "style": default_style_money},
            "D{}".format(row_category): {"value": 0, "style": default_style_money},
            "E{}".format(row_category): {"value": 0, "style": default_style_money},
        })
    
        i = 0
        for item in data:
            if item[0] == user:
                if item[2] == cate:
                    result.update({
                        "A{}".format(row): {"value": line_index, "style": default_style},
                        "B{}".format(row): {"value": item[5], "style": default_style},
                        "C{}".format(row): {"value": item[6], "style": default_style_money},
                        "D{}".format(row): {"value": item[7], "style": default_style_money},
                        "E{}".format(row): {"value": item[8], "style": default_style_money},
                    })
                    # cate data------------------
                    cate_price += item[6]
                    cate_discount += item[7]
                    cate_total += item[8]
                    # user data------------------
                    user_price += item[6]
                    user_discount += item[7]
                    user_total += item[8]
                    # -----------------------------
                    price_all += item[6]
                    discount_all += item[7]
                    total_all += item[8]
                    # -----------------------------
                    result.update({
                        "C{}".format(row_user_id): {"value": user_price, "style": user_style_money},
                        "D{}".format(row_user_id): {"value": user_discount, "style": user_style_money},
                        "E{}".format(row_user_id): {"value": user_total, "style": user_style_money},
                    })
                    result.update({
                        "A{}".format(row_category): {"value": cate_index, "style": category_style},
                        "B{}".format(row_category): {"value": item[3], "style": category_style},
                        "C{}".format(row_category): {"value": cate_price, "style": default_style_money},
                        "D{}".format(row_category): {"value": cate_discount, "style": default_style_money},
                        "E{}".format(row_category): {"value": cate_total, "style": default_style_money},
                    })
                    row += 1
                    line_index += 1
                else:
                    cate = item[2]
                    row_category = row
                    cate_index += 1
                    row += 1
                    line_index = 1
                    cate_price = 0
                    cate_discount = 0
                    cate_total = 0
                    result.update({
                        "A{}".format(row): {"value": line_index, "style": default_style},
                        "B{}".format(row): {"value": item[5], "style": default_style},
                        "C{}".format(row): {"value": item[6], "style": default_style_money},
                        "D{}".format(row): {"value": item[7], "style": default_style_money},
                        "E{}".format(row): {"value": item[8], "style": default_style_money},
                    })
                    # cate data------------------
                    cate_price += item[6]
                    cate_discount += item[7]
                    cate_total += item[8]
                    # user data------------------
                    user_price += item[6]
                    user_discount += item[7]
                    user_total += item[8]
                    # -----------------------------
                    price_all += item[6]
                    discount_all += item[7]
                    total_all += item[8]
                    # -----------------------------
                    result.update({
                        "C{}".format(row_user_id): {"value": user_price, "style": user_style_money},
                        "D{}".format(row_user_id): {"value": user_discount, "style": user_style_money},
                        "E{}".format(row_user_id): {"value": user_total, "style": user_style_money},
                    })

                    result.update({
                        "A{}".format(row_category): {"value": cate_index, "style": category_style},
                        "B{}".format(row_category): {"value": item[3], "style": category_style},
                        "C{}".format(row_category): {"value": cate_price, "style": default_style_money},
                        "D{}".format(row_category): {"value": cate_discount, "style": default_style_money},
                        "E{}".format(row_category): {"value": cate_total, "style": default_style_money},
                    })
                    row += 1
                    line_index += 1
            else:
                user = item[0]
                row_user_id = row
                row += 1
                cate = item[2]
                row_category = row
                row += 1
                cate_index = 1
                line_index = 1
                # -------------------------------
                cate_price = 0
                cate_discount = 0
                cate_total = 0
                # -------------------------------
                user_price = 0
                user_discount = 0
                user_total = 0

                result.update({
                    "A{}".format(row): {"value": line_index, "style": default_style},
                    "B{}".format(row): {"value": item[5], "style": default_style},
                    "C{}".format(row): {"value": item[6], "style": default_style_money},
                    "D{}".format(row): {"value": item[7], "style": default_style_money},
                    "E{}".format(row): {"value": item[8], "style": default_style_money},
                })
                # cate data------------------
                cate_price += item[6]
                cate_discount += item[7]
                cate_total += item[8]
                # user data------------------
                user_price += item[6]
                user_discount += item[7]
                user_total += item[8]
                # -----------------------------
                price_all += item[6]
                discount_all += item[7]
                total_all += item[8]
                # -----------------------------
                result.update({
                    "C{}".format(row_user_id): {"value": user_price, "style": user_style_money},
                    "D{}".format(row_user_id): {"value": user_discount, "style": user_style_money},
                    "E{}".format(row_user_id): {"value": user_total, "style": user_style_money},
                })
                user_result.append({"index": row_user_id, "data": item[1]})
                result.update({
                    "A{}".format(row_category): {"value": cate_index, "style": category_style},
                    "B{}".format(row_category): {"value": item[3], "style": category_style},
                    "C{}".format(row_category): {"value": cate_price, "style": default_style_money},
                    "D{}".format(row_category): {"value": cate_discount, "style": default_style_money},
                    "E{}".format(row_category): {"value": cate_total, "style": default_style_money},
                })
                row += 1
                line_index += 1
     
        return result, row, user_result, {"price": price_all, "discount": discount_all, "total": total_all}
        # # ----------------------------------------------------------------

    def get_data_from_sql(self, from_date, end_date, user_id, partner_id):
        query = " "
        if from_date: 
            query += "and orders.date_order>='" + \
                from_date.strftime("%Y-%m-%d")+"'"
        if end_date:
            query += "and orders.date_order<='" + \
                end_date.strftime("%Y-%m-%d")+"'"
        if user_id:
            query += "and users.id = "+str(user_id.id)
        if partner_id:
            query += "and partner.id = "+str(partner_id.id)
        self.env.cr.execute("""
            select user_id,user_name,categ_id,categ_name,partner_id,partner_name,
                sum(orderline.price_unit*orderline.product_uom_qty) as price,
                sum(((orderline.price_unit*orderline.product_uom_qty)*orderline.discount)/100) as discount,
                sum((orderline.price_unit*orderline.product_uom_qty)-(((orderline.price_unit*orderline.product_uom_qty)*orderline.discount)/100))as total
            from 
            (select users.id as user_id,users.name as user_name,
                cate.id as categ_id ,cate.name as categ_name, 
                partner.id as partner_id,partner.name as partner_name,
                lines.id as line_id
                from product_template as temps,
                    product_product as product,
                    product_category as cate,
                    (select res_users.id,res_partner.name from res_users,res_partner 
                    where res_users.partner_id =res_partner.id)as users,
                    sale_order as orders,
                    sale_order_line as lines,
                    res_partner as partner
                where temps.categ_id=cate.id and product.product_tmpl_id=temps.id 
                    and orders.id=lines.order_id and orders.user_id = users.id
                    and lines.product_id=product.id and orders.partner_id=partner.id """+query+"""
            group by users.id,users.name,cate.id,cate.name,partner.id,partner.name,lines.id
            order by users.id,cate.id,partner.id)as report,sale_order_line as orderline
            where orderline.id =report.line_id
            group by report.user_id,report.user_name,report.categ_id,report.categ_name,report.partner_id,report.partner_name
            order by user_id,categ_id,partner_id
        """)
        data = self.env.cr.fetchall()
        return data
