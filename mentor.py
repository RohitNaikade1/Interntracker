from Package import *
from datetime import *

def numOfDays(date1, date2):
    return (date1-date2).days

day=datetime.today().strftime('%A')

if day == "Saturday" or day == "Sunday":
    print("Enjoy weekend")
else:
    Mentors=db.Mentors
    data=Mentors.find({})
    for d in data:
        Interns=db.Interns
        
        for intern in d['interns']:
            data=Interns.find({"emailId":intern})
            
            for res in data:

                print(res['leaves'])

                flag=False
                for recs in res['leaves']:
                    if recs['date'] == date.today() and recs['remarks'] == "Approve":
                        flag=True
                if res['lastUpdate'] != date.today() and flag == False:
                    first=str(date.today())
                    date1 = datetime.strptime(first, "%Y-%m-%d")
                    d1=date1.day       
                    m1=date1.month    
                    y1=date1.year 

                    date2 = datetime.strptime(res['lastUpdate'], "%Y-%m-%d")
                    d2=date2.day       
                    m2=date2.month    
                    y2=date2.year 

                    date3 = date(y1,m1,d1)
                    date4 = date(y2,m2,d2)

                    diff=numOfDays(date3,date4)

                    if diff >= 3:
                        print("manager")
                    else:
                        print("Intern")
                        # msg = Message("You haven't updated your previous  "+ session['email'], sender = 'naikaderohit833@gmail.com', recipients = [intern['mentor']])
                        # msg.body = "You have received a leave application from " + session['email'] +".Login and Approve/Reject the same and notify him/her about Remark."
                        # mail.send(msg)             
