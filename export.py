import xlsxwriter
from Package import *
import os

def exportfile(email):

    dir_list = os.listdir("Package/static/Sheets/")
    print(os.getenv('host'))

    for file in dir_list:
        if email+".xlsx" == file:
            print("yes")
            return
    workbook = xlsxwriter.Workbook('Package/static/Sheets/'+email+'.xlsx')
    worksheet = workbook.add_worksheet("Plan")

    Intern=db.Interns

    data=Intern.find_one({"emailId":email})

    heads=['ModuleName','Assignments','subModule','PD','Status','startDate','endDate']
    rows=[]
    rows.append(heads)
    for modules in data['inductionPlan']['modules']:
        flag=True
        row=[modules['moduleName']]

        ass=""

        for d in modules['Assignments']:
            ass=ass+" "+d

        row.append(ass)
        for dt in modules['subModules']:
            if flag==True:
                row.append(dt['name'])
                row.append(dt['PD'])
                row.append(dt['status'])
                row.append(dt['startDate'])
                row.append(dt['endDate'])
                flag=False
            else:
                row.append("")
                row.append("")
                row.append(dt['name'])
                row.append(dt['PD'])
                row.append(dt['status'])
                row.append(dt['startDate'])
                row.append(dt['endDate'])
            rows.append(row)
            row=[]

    rowd = 0
    cold = 0

# Iterate over the data and write it out row by row.
    for ModuleName, Assignments,subModule,PD,Status,startDate,endDate in (rows):
        worksheet.write(rowd, cold, ModuleName)
        worksheet.write(rowd, cold + 1, Assignments)
        worksheet.write(rowd, cold+2, subModule)
        if isinstance(PD,float) and PD>=0.0 and PD<=100.0:
            worksheet.write(rowd, cold + 3, PD)
        elif isinstance(PD,str):
            worksheet.write(rowd, cold + 3, 'PD')
        else:
            worksheet.write(rowd, cold + 3, 0)

        worksheet.write(rowd, cold+4, Status)
        worksheet.write(rowd, cold + 5, startDate)
        worksheet.write(rowd, cold + 6, endDate)
        rowd += 1

    workbook.close()
pass


exportfile("naikaderohit833@gmail.com")
