import xlrd
rb = xlrd.open_workbook('bhrec.xls', formatting_info=True)
sheet = rb.sheet_by_index(0)
for rownum in range(2,sheet.nrows):
    row = sheet.row_values(rownum)
    for c_el in row:
        if c_el:
            print c_el
    print '-----------------'