from Package import *
from datetime import date
from datetime import timedelta as td
from datetime import datetime

Interns = db.Interns

data = Interns.find({})

for intern in data:

    for modules in intern['inductionPlan']['modules']:

        flag = True

        if 'deadline' in modules and modules['RKT'] == False and modules['deadline']!="":

            first = str(date.today())
            date1 = datetime.strptime(first, "%Y-%m-%d")
            date2 = datetime.strptime(modules['deadline'], "%Y-%m-%d")

            print(date1,date2)
            if date1 == date2:

                for sub in modules['subModules']:
                    if sub['status'] != 'Completed':
                        flag = False
                        break
            else:
                flag = False

        elif modules['RKT'] == False:
            for sub in modules['subModules']:

                if sub['status'] != 'Completed':
                    flag = False
                    break
        else:
            continue

        if flag == False:
            continue
        else:
            print(modules['moduleName'], intern['emailId'])
            to = [intern['emailId']]
            msg = EmailMessage()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                msg['Subject'] = 'Schedule an RKT!'
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = ','.join(to)
                msg.set_content("Schedule an RKT!")

                if 'fname' in intern and 'sname' in intern:
                    msg.add_alternative("""\

                    <!DOCTYPE html>
                        <body>
                            <h1> Hello """ + intern['fname'] + """ """+ intern['sname'] + """,</h1>
                                <p> You have successfully completed module <b>""" + modules['moduleName'] + """</b> from your induction plan. visit https://meet.google.com/ and schedule RKT on topic """+ modules['moduleName'] +""" </p>
                                <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                        </body>
                     </html>
                        """, subtype='html')

                else:
                    msg.add_alternative("""\

                    <!DOCTYPE html>
                        <body>
                            <h1> Hello """ + intern['emailId'] + """,</h1>
                                <p> You have successfully completed module <b>""" + modules['moduleName'] + """</b> from your induction plan. visit https://meet.google.com/ and schedule RKT on topic """+ modules['moduleName'] +""" </p>
                                <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                        </body>
                     </html>
                        """, subtype='html')

                smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

                smtp.send_message(msg)
                print("Email sent successfully!")
