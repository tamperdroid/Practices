import xlrd,xlsxwriter
li=["Daily1.xlsx","Daily2.xlsx"]
sheet_name=["Daily0","Daily1"]
wb = xlsxwriter.Workbook("file.xlsx")
for li_indx,xls in enumerate(li):
    print xls
    insheet=xlrd.open_workbook(xls)
    sheet_count = len(insheet.sheets())
    print sheet_count
    for c in range(sheet_count):
        outsheet = wb.add_worksheet(str(sheet_name[0]) + str(c)+str(li_indx))
        sh = insheet.sheet_by_index(c)
        for row_idx in xrange(sh.nrows):
            for col_idx in xrange(sh.ncols):
                outsheet.write(row_idx + 1, col_idx,
                               sh.cell_value(row_idx, col_idx))

wb.close()

"{%22AuctionTypeId%22:%22"+str(meta_id["Id"])+"%22,%22BorderIds%22:[" + str(border_id) + "],%22FromDate%22:%22{YYYY-1}-{MM-1}-{DD-1}T00:00:00%22,%22ToDate%22:%22{YYYY}-{MM}-{DD}T00:00:00%22,%22AuctionId%22:%22%22}"