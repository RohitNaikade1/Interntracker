from Package import *

@app.route("/deleteManager",methods=['POST'])
def deleteManager():
    if request.method == 'POST':
        email=request.form['email']
        Manager=db.Managers
        Mentor=db.Mentors

        Mentor.update_many({"manager":email},{"$set":{"manager":None}})

        Manager.delete_one({"emailId":email})
        
        manager=Manager.find({})

        return render_template('admin.html',managers=manager)
    else:
        Manager=db.Managers
        manager=Manager.find({})

        return render_template('admin.html',managers=manager)


@app.route("/manager",methods=['POST','GET'])
def managerPage():
    error=""
    if request.method=='POST':
        mentor=request.form['mentor']
        manager=request.form['manager']
        password=request.form['password']

        mentorDB=db.Mentors
        managerDB=db.Managers
        mentorColl=mentorDB.find_one({"emailId":mentor})
        managerColl=managerDB.find_one({"emailId":manager})
        if mentorColl:
            error="Mentor already exists"
        elif managerColl is None:
            error="Manager does not exist"
        else:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf8'), salt)
            mentorDB.insert_one({"emailId":mentor,"password":hashed,"manager":manager})
            managerDB.update_one({"emailId":manager},{'$push':{"mentors":mentor}},upsert=True)

            msg = EmailMessage()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                msg['Subject'] = 'Your Mentor Account is created Successfully on InternTracker under Manager ' + manager
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = mentor
                msg.add_alternative("""\

                            <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + mentor + """,</h1>
                                        <p> Your Email address is """ + mentor + """ And Password is """ + password + """</p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                    </html>
                                    """, subtype='html')

                smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

                smtp.send_message(msg)

            error="Mentor added Successfully"
            return render_template('manager.html',error=error)
        return render_template('manager.html',error=error)
    else:
        Mentors=db.Mentors
        mentor=Mentors.find({})
        return render_template('manager.html',mentors=mentor)