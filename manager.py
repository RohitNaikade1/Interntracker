from Package import *
from datetime import *

Managers=db.Managers

data=Managers.find({})

for d in data:
    if d['nextDate'] == date.today():
        
        pass
    else:
        for mentor in d['mentors']:
            Interns=db.Interns
            intern=Interns.find({"mentor":mentor})
            for d in intern:
                print(d['inductionPlan']['modules'])
        pass