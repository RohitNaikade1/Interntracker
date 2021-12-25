from Package import *
from datetime import *
import pandas as pd
from pretty_html_table import build_table
from send_mail import send_mail
from getPD import get_gdp_data

Managers = db.Managers

data = Managers.find({})

for manager in data:
    if manager['nextDate'] == date.today():

        managerModules = []
        managerPercent = []
        managerName = []
        managerEmail = []

        for mentor in manager['mentors']:
            Interns = db.Interns
            intern = Interns.find({"mentor": mentor})

            for d in intern:
                managerModules.append(d['inductionPlan']['name'])

                if 'fname' in d and 'sname' in d:
                    managerName.append(d['fname']+" "+d['sname'])
                    managerEmail.append(d['emailId'])
                else:
                    managerName.append("Not updated")
                    managerEmail.append(d['emailId'])

                temp = []
                for module in d['inductionPlan']['modules']:
                    completed = 0
                    for mdl in module['subModules']:
                        if mdl['status'] == 'Completed':
                            completed = completed+1

                    temp.append(
                        (completed/len(module['subModules']))*100)

                managerPercent.append(
                    str(int(sum(temp)/len(d['inductionPlan']['modules'])))+"%")

        data = get_gdp_data(managerModules, managerPercent,
                            managerName, managerEmail)
        output = build_table(data, 'blue_light')
        subject = "Induction stats!"
        receiver = [manager['emailId']]
        send_mail(output, subject, receiver)
        print(receiver)

        if manager['notifications'] == "Once in a week":
            today = datetime.date.today()
            Managers.update_one({"emailId": manager['emailId']}, {"$set": {"nextDate": str(
                today + datetime.timedelta(days=-today.weekday(), weeks=1))}})
        else:
            today = datetime.date.today()
            Managers.update_one({"emailId": manager['emailId']}, {"$set": {"nextDate": str(
                today + datetime.timedelta(days=-today.weekday(), weeks=2))}})
        pass
    else:
        pass
