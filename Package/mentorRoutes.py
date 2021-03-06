import datetime
from Package import *

@app.route("/deleteMentor",methods=['GET','POST'])
def deleteMentor():
    error=""
    if "email" in session and session['type']=="Managers" or session['type']=="Admin":
        if request.method == 'POST':
            email=request.form['email']

            try:
                Mentor=db.Mentors
                Managers=db.Managers
                Interns=db.Interns

                mentorData=Mentor.find_one({"emailId":email})
                Interns.update_many({"mentor":email},{"$set":{"mentor":None}})
                Managers.update_one({"emailId":mentorData['manager']},{"$pull":{"mentors":email}})
                
                Mentor.delete_one({"emailId":email})
              
                mentor=Mentor.find({})
                data={
                    "error":"Mentor deleted successfully",
                    "mentors":mentor
                    }

                return render_template('manager.html',mentors=data)
            except:
                mentor=Mentor.find({})
                data={
                    "error":"error occurred!",
                    "mentors":mentor
                    }

                return render_template('manager.html',mentors=data)
        else:
            Mentor=db.Mentors
            mentor=Mentor.find({})
            data={
                    "mentors":mentor
                }

            return render_template('manager.html',mentors=data)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"
        
@app.route("/mentor",methods=['POST','GET'])
def mentorPage():

    if "email" in session and session['type']=="Mentors" or session['type']=="Managers" or session['type']=="Admin":
        error=""
        if request.method=='POST':
            intern=request.form['intern']
            mentor=request.form['mentor']
            plan=request.form['plan']
            password=request.form['password']
            print("@"+plan+"@")
            plan=db.Plans.find_one({'name':request.form['plan']})
            print(plan)
            if plan is None:
                Interns=db.Interns
                error="Plan does not exist"
                intern=Interns.find({})
                data={
                    "error":error,
                    "interns":intern,
                    "plans":[]
                }
                plans=db.Plans.find({})
                for res in plans:
                    data['plans'].append(res['name'])
                return render_template('mentor.html',data=data)


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
                internDB.insert_one({"emailId":intern,"password":hashed,"salt":salt,"inductionPlan":plan,"mentor":mentor,"lastUpdate":str(datetime.date.today()),"leaves":[]})
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
                Interns=db.Interns
                intern=Interns.find({})
                data={
                    "error":error,
                    "interns":intern,
                    "plans":[]
                }
                plans=db.Plans.find({})
                for res in plans:
                    data['plans'].append(res['name'])
                return render_template('mentor.html',data=data)
            Interns=db.Interns
            intern=Interns.find({})
            data={
                    "error":error,
                    "interns":intern,
                    "plans":[]
                }
            plans=db.Plans.find({})
            for res in plans:
                data['plans'].append(res['name'])
            return render_template('mentor.html',data=data)
        else:

            Interns=db.Interns
            intern=Interns.find({})
            data={
                    "interns":intern,
                    "plans":[]
                }
            plans=db.Plans.find({})
            for res in plans:
                data['plans'].append(res['name'])
            return render_template('mentor.html',data=data)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"