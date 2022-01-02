import datetime
from Package import *

@app.route("/deleteMentor",methods=['POST'])
def deleteMentor():

    if "email" in session and session['type']=="Managers":
        if request.method == 'POST':
            email=request.form['email']
            Mentor=db.Mentors
            Managers=db.Managers
            Interns=db.Interns

            Interns.update_many({"mentor":email},{"$set":{"mentor":None}})
            Managers.update_one({"emailId":session['email']},{"$pull":{"mentors":email}})
            Mentor.delete_one({"emailId":email})
            mentor=Mentor.find({})

            return render_template('manager.html',mentors=mentor)
        else:
            Mentor=db.Mentors
            mentor=Mentor.find({})

            return render_template('manager.html',mentors=mentor)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"
        
@app.route("/mentor",methods=['POST','GET'])
def mentorPage():

    if "email" in session and session['type']=="Managers":
        error=""
        if request.method=='POST':
            intern=request.form['intern']
            mentor=request.form['mentor']
            plan=request.form['plan']
            password=request.form['password']

            Plan=db.Plans
            plan=Plan.find_one({'name':plan})
            if plan is None:
                error="Plan does not exist"
                return render_template('mentor.html',error=error)

            internDB=db.Interns
            mentorDB=db.Mentors
            internColl=internDB.find_one({"emailId":intern})
            mentorColl=mentorDB.find_one({"emailId":mentor})
            if internColl:
                error="Intern already exists"
            elif mentorColl is None:
                error="Mentor does not exist"
            else:
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                internDB.insert_one({"emailId":intern,"password":hashed,"inductionPlan":plan,"mentor":mentor,"lastUpdate":str(datetime.date.today()),"leaves":[]})
                mentorDB.update_one({"emailId":mentor},{'$push':{"interns":intern}},upsert=True)

                msg = EmailMessage()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                    msg['Subject'] = 'Your Intern Account is created Successfully on InternTracker under Mentor ' + mentor +'.'
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = intern
                    msg.add_alternative("""\

                            <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + intern + """,</h1>
                                        <p>Login on InternTracker portal and check your induction plan Named """+ plan['name'] +"""</p>
                                        <p> Your Email address is """ + intern + """ And Password is """ + password + """</p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                    </html>
                                    """, subtype='html')

                    smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

                    smtp.send_message(msg)
                error="Intern added Successfully"
                return render_template('mentor.html',error=error)
            return render_template('mentor.html',error=error)
        else:

            Interns=db.Interns
            intern=Interns.find({})
            return render_template('mentor.html',interns=intern)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"