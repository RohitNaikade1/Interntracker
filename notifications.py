from dns.rdatatype import NULL
from Package import *
from datetime import *

def numOfDays(date1, date2):
    return (date1-date2).days


day = datetime.today().strftime('%A')

if day == "Saturday" or day == "Sunday":
    pass
else:
    Mentors = db.Mentors
    data = Mentors.find({})
    for d in data:
        Interns = db.Interns

        for intern in d['interns']:
            data = Interns.find({"emailId": intern})

            for res in data:

                flag = False
                first = str(date.today())
                temp1 = datetime.strptime(first,"%Y-%m-%d")
                for recs in res['leaves']:

                    temp2 = datetime.strptime(recs['date'], "%Y-%m-%d")
                    if 'remarks' in recs and temp1==temp2 and recs['remarks'] == "Approve":
                        flag = True
                
                temp3 = datetime.strptime(res['lastUpdate'], "%Y-%m-%d")
                if temp1 != temp3 and flag == False:
                    first = str(date.today())
                    date1 = datetime.strptime(first, "%Y-%m-%d")
                    d1 = date1.day
                    m1 = date1.month
                    y1 = date1.year

                    date2 = datetime.strptime(res['lastUpdate'], "%Y-%m-%d")
                    d2 = date2.day
                    m2 = date2.month
                    y2 = date2.year

                    date3 = date(y1, m1, d1)
                    date4 = date(y2, m2, d2)

                    diff = numOfDays(date3, date4)

                    if day == "Monday":
                        diff = diff-2

                    if diff >= 3:

                        to = [d['manager'], d['emailId']]
                        msg = EmailMessage()

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                            msg['Subject'] = 'Induction Plan Updates!'
                            msg['From'] = EMAIL_ADDRESS
                            msg['To'] = ','.join(to)
                            msg.set_content("Hello "+d['manager']+", The intern with email address " + res['emailId'] +
                                            " haven't updated induction plan sheet from last 3 days.plaese take a look!")

                            Managers = db.Managers
                            managerRec = Managers.find_one(
                                {"emailId": d['manager']})

                            if 'fname' in managerRec:

                                if 'fname' in res:
                                    msg.add_alternative("""\

                                    <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + managerRec['fname'] + """,</h1>
                                        <p> The intern """ + res['fname'] +" "+ res['sname'] + """ with email address """+ res['emailId']+ """ haven't updated induction plan sheet from last 3 days.plaese take a look!</p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                </html>
                                """, subtype='html')

                                else:
                                    msg.add_alternative("""\

                                    <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + managerRec['fname'] + """,</h1>
                                        <p> The intern with email address """ + res['emailId'] + """ haven't updated induction plan sheet from last 3 days.plaese take a look!</p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                </html>
                                """, subtype='html')
                            else:
                                if 'fname' in res:
                                    msg.add_alternative("""\

                                    <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + managerRec['fname'] + """,</h1>
                                        <p> The intern """ + res['fname'] +" "+ res['sname'] + """ with email address """+ res['emailId']+ """ haven't updated induction plan sheet from last 3 days.plaese take a look!</p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                    </html>
                                    """, subtype='html')

                                else:
                                    msg.add_alternative("""\

                                    <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + managerRec['fname'] + """,</h1>
                                        <p> The intern with email address """ + res['emailId'] + """ haven't updated induction plan sheet from last 3 days.plaese take a look!</p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                </html>
                                """, subtype='html')

                            smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

                            smtp.send_message(msg)
                        

                    else:

                       
                        msg = EmailMessage()

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                            msg['Subject'] = 'Induction Plan Updates!'
                            msg['From'] = EMAIL_ADDRESS
                            msg['To'] = res['emailId']
                            msg.set_content("Yes Reached")

                            if 'fname' in res:
                                    msg.add_alternative("""\

                                    <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + res['fname'] +" "+ res['sname'] +  """,</h1>
                                        <p> You haven't updated today's induction plan sheet.update it ASAP!</p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                    </html>
                                    """, subtype='html')

                            else:
                                    msg.add_alternative("""\

                                    <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + res['emailId'] + """,</h1>
                                        <p> You haven't updated today's induction plan sheet.update it ASAP!</p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                </html>
                                """, subtype='html')

                            smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

                            smtp.send_message(msg)
                       

                elif res['lastUpdate'] == "":
                        
                        msg = EmailMessage()

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                            msg['Subject'] = 'Induction Plan Updates!'
                            msg['From'] = EMAIL_ADDRESS
                            msg['To'] = res['emailId']
                            msg.set_content("Yes Reached")

                            if 'fname' in res:
                                    msg.add_alternative("""\

                                    <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + res['fname'] +" "+ res['sname'] +  """,</h1>
                                        <p> You haven't updated today's induction plan sheet.update it ASAP!</p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                    </html>
                                    """, subtype='html')

                            else:
                                    msg.add_alternative("""\

                                    <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + res['emailId'] + """,</h1>
                                        <p> You haven't updated today's induction plan sheet.update it ASAP!</p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                </html>
                                """, subtype='html')

                            smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

                            smtp.send_message(msg)
                
                elif flag == True:

                       
                        
                        Interns.update_one({"emailId": intern}, {
                                       "lastUpdate": date.today()})
