from Package import *


@app.route("/deleteManager", methods=['POST'])
def deleteManager():

    if "email" in session and session['type'] == "Admin":
        error = ""
        if request.method == 'POST':
            email = request.form['email']

            try:
                Manager = db.Managers
                Mentor = db.Mentors

                Mentor.update_many({"manager": email}, {
                                   "$set": {"manager": None}})

                Manager.delete_one({"emailId": email})

                manager = Manager.find({})
                error = "Manager deleted Successfully"

                data = {
                    "error": error,
                    "managers": manager
                }
                return render_template('admin.html', managers=data)
            except:
                manager = Manager.find({})
                error = "Error occurred!"

                data = {
                    "error": error,
                    "managers": manager
                }
                return render_template('admin.html', managers=data)
        else:
            Manager = db.Managers
            manager = Manager.find({})
            data = {
                "managers": manager
            }
            return render_template('admin.html', managers=data)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"


@app.route("/manager", methods=['POST', 'GET'])
def managerPage():

    if "email" in session and session['type'] == "Managers" or session['type'] == "Admin":
        error = ""
        if request.method == 'POST':
            mentor = request.form['mentor']
            manager = request.form['manager']
            password = request.form['password']

            try:
                mentorDB = db.Mentors
                managerDB = db.Managers
                mentorColl = mentorDB.find_one({"emailId": mentor})
                managerColl = managerDB.find_one({"emailId": manager})
                if mentorColl:
                    error = "Mentor already exists"
                elif managerColl is None:
                    error = "Manager does not exist"
                else:
                    salt = bcrypt.gensalt()
                    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                    mentorDB.insert_one(
                        {"emailId": mentor, "password": hashed,"salt":salt, "manager": manager})
                    managerDB.update_one({"emailId": manager}, {
                                         '$push': {"mentors": mentor}}, upsert=True)

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

                    error = "Mentor added Successfully"

                    mentor = mentorDB.find({})
                    data = {
                        "error": error,
                        "mentors": mentor
                    }
                    return render_template('manager.html', mentors=data)
            except:
                mentor = mentorDB.find({})
                data = {
                    "error": "Error occurred!",
                    "mentors": mentor
                }
                return render_template('manager.html', mentors=data)
        else:
            Mentors = db.Mentors
            mentor = Mentors.find({})
            data = {
                "mentors": mentor
            }
            return render_template('manager.html', mentors=data)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"
