from Package import *
from datetime import *
import smtplib

def numOfDays(date1, date2):
    return (date1-date2).days

gmail_user = 'rohit.naikade@gslab.com'
gmail_password = 'vgshfwkiyxjrnuyp'

sent_from = gmail_user

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
                    
                    if day == "Monday":
                        diff=diff-2

                    if diff >= 3:

                        subject = 'Induction Plan!'
                        body = "Hello "+d['manager']+", The intern with email address "+ res['emailId']+" haven't updated induction plan sheet from last 3 days.plaese take a look!"

                        email_text = """\
                        From: %s
                        To: %s
                        Subject: %s

                        %s\
                        """ % (sent_from, d['manager'], subject, body)

                        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                        smtp_server.ehlo()
                        smtp_server.login(gmail_user, gmail_password)
                        smtp_server.sendmail(sent_from, d['manager'], email_text)
                        smtp_server.close()
                        print ("Email sent successfully!")   

                    else:
                        
                        print("Intern")
                        subject = 'Induction Plan!'
                        body = "Hello "+res['emailId']+",You haven't updated your today's induction work on induction plan.update it by tomorrow morning itself."

                        email_text = """\
                        From: %s
                        To: %s
                        Subject: %s

                        %s\
                        """ % (sent_from, res['emailId'], subject, body)

                        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                        smtp_server.ehlo()
                        smtp_server.login(gmail_user, gmail_password)
                        smtp_server.sendmail(sent_from, res['emailId'], email_text)
                        smtp_server.close()
                        print ("Email sent successfully!")    
                               
                elif flag == True:
                    Interns.update_one({"emailId":intern},{"lastUpdate":date.today()})