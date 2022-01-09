import xlsxwriter
from Package import *
import os
from datetime import date
from datetime import timedelta as td
from datetime import datetime
from pretty_html_table import build_table
from send_mail import send_mail
from getPD import get_gdp_data

print(str(date.today()))


def exportfile(email):

    # dir_list = os.listdir("Package/static/Sheets/")

    # for file in dir_list:
    #     if email+".xlsx" == file:
    #         print("yes")
    #         return
    workbook = xlsxwriter.Workbook('Package/static/Sheets/'+email+'.xlsx')
    worksheet = workbook.add_worksheet("Plan")

    Intern = db.Interns

    data = Intern.find_one({"emailId": email})

    heads = ['ModuleName', 'Assignments', 'subModule',
             'PD', 'Status', 'startDate', 'endDate']
    rows = []
    rows.append(heads)
    for modules in data['inductionPlan']['modules']:
        flag = True
        row = [modules['moduleName']]

        ass = ""

        for d in modules['Assignments']:
            ass = ass+" "+d

        row.append(ass)
        for dt in modules['subModules']:
            if flag == True:
                row.append(dt['name'])
                row.append(dt['PD'])
                row.append(dt['status'])
                row.append(dt['startDate'])
                row.append(dt['endDate'])
                flag = False
            else:
                row.append("")
                row.append("")
                row.append(dt['name'])
                row.append(dt['PD'])
                row.append(dt['status'])
                row.append(dt['startDate'])
                row.append(dt['endDate'])
            rows.append(row)
            row = []

    rowd = 0
    cold = 0

    for ModuleName, Assignments, subModule, PD, Status, startDate, endDate in (rows):
        worksheet.write(rowd, cold, ModuleName)
        worksheet.write(rowd, cold + 1, Assignments)
        worksheet.write(rowd, cold+2, subModule)
        if isinstance(PD, float) and PD >= 0.0 and PD <= 100.0:
            worksheet.write(rowd, cold + 3, PD)
        elif isinstance(PD, str):
            worksheet.write(rowd, cold + 3, 'PD')
        else:
            worksheet.write(rowd, cold + 3, 0)

        worksheet.write(rowd, cold+4, Status)
        worksheet.write(rowd, cold + 5, startDate)
        worksheet.write(rowd, cold + 6, endDate)
        rowd += 1

    workbook.close()


Mentors = db.Mentors

data = Mentors.find({})

for mentor in data:

    if 'nextDate' in mentor:
        first = str(date.today())
        date1 = datetime.strptime(first, "%Y-%m-%d")
        date2 = datetime.strptime(mentor['nextDate'], "%Y-%m-%d")

        if date1 == date2:

            Interns = db.Interns
            intern = Interns.find({"mentor": mentor['emailId']})

            modules = []
            name = []
            email = []
            percentage = []
            files = []

            for d in intern:
                modules.append(d['inductionPlan']['name'])
                exportfile(d['emailId'])
                files.append(os.getenv('host')+'static/Sheets/' +
                             d['emailId']+'.xlsx')

                if 'fname' in d and 'sname' in d:
                    name.append(d['fname']+" "+d['sname'])
                    email.append(d['emailId'])
                else:
                    name.append("Not updated")
                    email.append(d['emailId'])

                temp = []
                for module in d['inductionPlan']['modules']:
                    completed = 0
                    for mdl in module['subModules']:
                        if mdl['status'] == 'Completed':
                            completed = completed+1

                    temp.append(
                        (completed/len(module['subModules']))*100)

                percentage.append(
                    str(int(sum(temp)/len(d['inductionPlan']['modules'])))+"%")
            data = get_gdp_data(modules, percentage, name, email, files)
            output = build_table(data, 'blue_light')
            subject = "Induction stats!"
            receiver = [mentor['emailId']]
            send_mail(output, subject, receiver)

            if mentor['notifications'] == "Once in a week":
                today = date.today()
                Mentors.update_one({"emailId": mentor['emailId']}, {"$set": {"nextDate": str(
                    today + td(days=-today.weekday(), weeks=1))}})
            else:
                today = date.today()
                Mentors.update_one({"emailId": mentor['emailId']}, {"$set": {"nextDate": str(
                    today + td(days=-today.weekday(), weeks=2))}})

            pass
        else:

            pass
    else:
        to = [mentor['emailId']]
        msg = EmailMessage()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

            msg['Subject'] = 'Update your profile to get induction updates!'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = ','.join(to)
            msg.set_content("Schedule an RKT!")

            msg.add_alternative("""\

                    <!DOCTYPE html>
                        <body>
                            <h1> Hello """ + mentor['emailId'] + """,</h1>
                                <p> You haven't updated your profile details yet.update profile details to get induction updates/completion status of interns. </p>
                                <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                        </body>
                     </html>
                        """, subtype='html')

            smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

            smtp.send_message(msg)
