import base64
import io
from odoo import models


class BaoCaoChamCong(models.AbstractModel):
    _name = 'report.cham_cong_fostech.report_cham_cong_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):

        sheet = workbook.add_worksheet('lsts')
        text_top_style = workbook.add_format(
            {'font_size': 12, 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'align': 'center'})
        text_header_style = workbook.add_format({'font_size': 12, 'bold': True, 'font_color': 'white',
                                                'bg_color': '#595959', 'valign': 'vcenter', 'text_wrap': False, 'align': 'center', 'border': 2})
        text_style = workbook.add_format(
            {'font_size': 12, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'border': 1})
        merge_style1 = workbook.add_format(
            {'font_size': 12, 'valign': 'vcenter', 'text_wrap': False, 'align': 'center', 'bold': True, 'border': 0})
        merge_style2 = workbook.add_format(
            {'font_size': 12, 'valign': 'vcenter', 'text_wrap': False, 'align': 'center', 'border': 0})
        number_style = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'num_format': '@', 'text_wrap': True, 'border': 1})
        sheet.set_column('A:A', 5)
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 12)
        sheet.set_column('E:E', 12)
        sheet.set_column('F:F', 10)
        sheet.set_column('G:G', 10)
        sheet.set_column('H:H', 10)
        sheet.set_column('I:I', 10)
        sheet.set_column('J:J', 10)
        sheet.set_column('K:K', 20)
        sheet.set_column('L:L', 25)
        sheet.set_column('M:M', 20)
        sheet.set_column('N:N', 45)
        sheet.set_column('O:O', 20)

        row = 0
        col = 0

        sheet.merge_range(
            'A1:O1',    'BẢNG CHẤM CÔNG CÔNG TY TNHH MTV CÔNG NGHỆ FOS', merge_style1)
        sheet.merge_range('A2:O2',    'Tháng 10 năm 2022', merge_style2)

        row = 2
        col = 0

        header = ['STT', 'Mã(CODE)', 'Họ và tên', 'Bộ phận',
                  'Không lương', 'Nghỉ phép có lương', 'Nửa ngày có lương', 'Nửa ngày không lương', 'Ngày công', 'Nghỉ lễ', 'Số ngày phép nhân viên', 'Số phép còn lại của nhân viên', 'Ngày công tính lương', 'Ghi chú', 'Ký xác nhận']
        sheet.write_row(row, 0, header, text_header_style)

        stt = 0
        for r in data['lst']:
            row += 1
            stt += 1
            sheet.write(row, col, stt, text_style)
            sheet.write(row, col+1, r['ma_nhan_vien'], number_style)
            sheet.write(row, col+2, r['nhan_vien'], text_style)
            sheet.write(row, col+3, r['bo_phan'], text_style)
            sheet.write(row, col+4, r['khong_luong'], number_style)
            sheet.write(row, col+5, r['so_phep'], number_style)
            sheet.write(row, col+6, r['nua_ngay'], number_style)
            sheet.write(row, col+7, r['tru_nua'], number_style)
            sheet.write(row, col+8, r['cong_ngay'], number_style)
            sheet.write(row, col+9, r['nghi_le'], number_style)
            sheet.write(row, col+10, r['so_phep_cua_nhan_vien'], number_style)
            sheet.write(
                row, col+11, r['so_phep_con_lai_nhan_vien'], number_style)
            sheet.write(row, col+12, r['ngay_cong_tinh_luong'], number_style)
            sheet.write(row, col+13, r['ghi_chu'], text_style)
            sheet.write(row, col+14, r['ky_xac_nhan'], text_style)
