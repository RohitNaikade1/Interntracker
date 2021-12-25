from Package import *
from datetime import *
from pretty_html_table import build_table
from send_mail import send_mail
from getPD import get_gdp_data

Mentors = db.Mentors

data = Mentors.find({})

for mentor in data:
    if mentor['nextDate'] == date.today():

        Interns = db.Interns
        intern = Interns.find({"mentor": mentor['emailId']})

        modules = []
        name = []
        email = []
        percentage = []

        for d in intern:
            modules.append(d['inductionPlan']['name'])

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
            print(temp, sum(temp), len(d['inductionPlan']['modules']))
            percentage.append(
                str(int(sum(temp)/len(d['inductionPlan']['modules'])))+"%")
        data = get_gdp_data(modules, percentage, name, email)
        output = build_table(data, 'blue_light')
        subject = "Induction stats!"
        receiver = [mentor['emailId']]
        send_mail(output, subject, receiver)
        print(receiver)


        if mentor['notifications'] == "Once in a week":
            today = datetime.date.today()
            Mentors.update_one({"emailId": mentor['emailId']}, {"$set": {"nextDate": str(
                today + datetime.timedelta(days=-today.weekday(), weeks=1))}})
        else:
            today = datetime.date.today()
            Mentors.update_one({"emailId": mentor['emailId']}, {"$set": {"nextDate": str(
                today + datetime.timedelta(days=-today.weekday(), weeks=2))}})

        pass
    else:

        pass
        
