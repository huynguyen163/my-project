from odoo import models
import base64
import io


class PatientCardXlsx(models.AbstractModel):
    _name = 'report.ft_report_project.report_project_id_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    

    def generate_xlsx_report(self, workbook, data, projects ):
        sheet = workbook.add_worksheet('Báo cáo dự án')
        text_top_style = workbook.add_format(
            {'font_size': 12, 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'align': 'center'})
        text_header_style = workbook.add_format({'font_size': 12, 'bold': True, 'font_color': 'black',
                                                'bg_color': '#33CCFF', 'valign': 'vcenter', 'text_wrap': False, 'align': 'center', 'border': 2})
        text_style = workbook.add_format(
            {'font_size': 12, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'border': 1})
        merge_style1 = workbook.add_format(
            {'font_size': 25, 'valign': 'vcenter', 'font_color': '#33CCFF', 'text_wrap': False, 'align': 'center', 'bold': True})
        merge_style2 = workbook.add_format(
            {'font_size': 12, 'valign': 'vcenter', 'text_wrap': False, 'align': 'center', 'border': 0})
        number_style = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'num_format': '@', 'text_wrap': True, 'border': 1})
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 20)

        row=0
        col=0
        sheet.merge_range('A1:G2',data['project'],merge_style1)
        
        

        row = 4
        col = 0
        sheet.write_row(row,col,['Assigned To'],workbook.add_format({'font_size': 14, 'align': 'center','bold': True}))
        sheet.write_row(row,col+2,['Stage'],workbook.add_format({'font_size': 14, 'align': 'center','bold': True}))
        sheet.write_row(row,col+4,['Start Date'],workbook.add_format({'font_size': 14, 'align': 'center','bold': True}))
        sheet.write_row(row,col+6,['End Date'],workbook.add_format({'font_size': 14, 'align': 'center','bold': True}))

        row = 5
        col = 0
        sheet.write(row,col,data['user_id'],workbook.add_format({'font_size': 14, 'align': 'center'}))
        sheet.write(row,col+2,data['stage'],workbook.add_format({'font_size': 14, 'align': 'center'}))
        sheet.write(row,col+4,data['start_date'],workbook.add_format({'font_size': 14, 'align': 'center'}))
        sheet.write(row,col+6,data['end_date'],workbook.add_format({'font_size': 14, 'align': 'center'}))
            
        



        row = 8
        col = 0
        header2 = ['Task Name','Assigned To','Assigning Date','Deadline','Planned Hours','Spent Hours','Remaining Hours']
        sheet.write_row(row,0,header2,text_header_style)
        for r in data['projects']:
            row += 1
            sheet.write(row,col,r['name'],text_style)
            sheet.write(row,col+1,r['portal_user_names'],text_style)
            sheet.write(row,col+2,r['date_assign'],number_style)
            sheet.write(row,col+3,r['date_deadline'],number_style)
            sheet.write(row,col+4,r['planned_hours'],number_style)
            sheet.write(row,col+5,'',number_style)
            sheet.write(row,col+6,'',number_style)
            
            
            
            
