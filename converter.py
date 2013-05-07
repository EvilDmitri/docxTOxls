import xlwt
wbk = xlwt.Workbook()
black_borders = xlwt.Borders()
black_borders.left = xlwt.Borders.THIN # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
black_borders.right = xlwt.Borders.THIN
black_borders.top = xlwt.Borders.THIN
black_borders.bottom = xlwt.Borders.THIN
black_borders.left_colour = 0x40
black_borders.right_colour = 0x40
black_borders.top_colour = 0x40
black_borders.bottom_colour = 0x40


blue_borders = xlwt.Borders()
blue_borders.left = xlwt.Borders.THIN # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
blue_borders.right = xlwt.Borders.THIN
blue_borders.top = xlwt.Borders.THIN
blue_borders.bottom = xlwt.Borders.THIN
blue_borders.left_colour = 0x10
blue_borders.right_colour = 0x10
blue_borders.top_colour = 0x10
blue_borders.bottom_colour = 0x10

yellow_pattern = xlwt.Pattern() # Create the Pattern
yellow_pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
yellow_pattern.pattern_fore_colour = 5 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green,

white_pattern = xlwt.Pattern() # Create the Pattern
white_pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
white_pattern.pattern_fore_colour = 1


header_style = xlwt.XFStyle() # Create Style
header_style.borders = black_borders # Add Borders to Style
header_style.pattern = yellow_pattern # Add Pattern to Style

style = xlwt.XFStyle()
style.borders = black_borders
style.pattern = white_pattern

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

    first_dict = dict()
    row_number = 0
    for row in first_table.iterchildren():
        line = getdocumenttext(row)

        if line:
            if line.__len__() == 2:
                first_dict[line[0]] = line[1]

            elif line.__len__() == 1:
                first_dict[line[0]] = ''

            else:
                first_dict[line[0]] = ''.join(line[1:])

        # if line.__len__():
        #     col_number = 0
        #     for cell in line:
        #         sheet_1.write(row_number, col_number, cell.strip())
        #         col_number += 1

        row_number += 1

    print first_dict


def parse_second_table():
    second_table = tblList[1]
    row_number = 0

    new_rows = []

    for row in second_table:
        line = getdocumenttext(row)
        if line:

            if line.__len__() == 1:
                sheet_1.write_merge(row_number, row_number, 4, 8, line[0], header_style)


            elif line.__len__() > 3:
                col_number = 4
                for cell in line:
                    sheet_1.write(row_number, col_number, cell.strip(), style)
                    col_number += 1



            row_number += 1


#parse_first_table()
parse_second_table()
wbk.save('test.xls')
