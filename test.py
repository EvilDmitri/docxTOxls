import xlwt
wbk = xlwt.Workbook()
borders = xlwt.Borders()
borders.left = xlwt.Borders.THIN # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
borders.right = xlwt.Borders.THIN
borders.top = xlwt.Borders.THIN
borders.bottom = xlwt.Borders.THIN
borders.left_colour = 0x40
borders.right_colour = 0x40
borders.top_colour = 0x40
borders.bottom_colour = 0x40

style = xlwt.XFStyle() # Create Style
style.borders = borders # Add Borders to Style


sheet_1 = wbk.add_sheet('sheet 1')
sheet_2 = wbk.add_sheet('sheet 2')

sheet_1.col(0).width = 9999
sheet_1.col(1).width = 9999

# Import the module
from docx import *

# Open the .docx file
document = opendocx('bhrec.docx')

# Load tables
tblList = document.xpath('//w:tbl', namespaces=document.nsmap)

def parse_first_table():
    first_table = tblList[0]
    row_number = 0
    for row in first_table.iterchildren():
        line = getdocumenttext(row)
        if line.__len__():
            col_number = 0
            for cell in line:
                sheet_1.write(row_number, col_number, cell.strip(), style)
                col_number += 1

        row_number += 1


def parse_second_table():
    second_table = tblList[1]
    row_number = 0
    for row in second_table:
        line = getdocumenttext(row)
        if line.__len__():

            if line.__len__() == 1:
                sheet_2.write_merge(row_number, row_number, 0, 4, line[0])

            elif line.__len__() > 4:
                col_number = 0
                for cell in line:
                    sheet_2.write(row_number, col_number, cell.strip())
                    col_number += 1



            row_number += 1


parse_first_table()
parse_second_table()
wbk.save('test.xls')
