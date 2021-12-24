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

        pass
    else:
        for mentor in manager['mentors']:
            Interns = db.Interns
            intern = Interns.find({"mentor": mentor})

            for d in intern:
                modules = []
                percentage = []
                for module in d['inductionPlan']['modules']:
                    completed = 0
                    for mdl in module['subModules']:
                        if mdl['status'] == 'Completed':
                            completed = completed+1
                    modules.append(module['moduleName'])
                    percentage.append(
                        str(int(completed/len(module['subModules'])*100))+"%")
                data = get_gdp_data(modules, percentage)
                output = build_table(data, 'blue_light')
                subject = "Induction stats for "+d['fname'] + " "+d['sname']
                receiver = [mentor, manager['emailId']]
                send_mail(output, subject, receiver)
                print(receiver)
        pass
