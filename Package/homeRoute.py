from Package import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@app.route("/logout")
def Logout():

    if "email" in session:
        error = "You have signed out successfully!"
        session.pop('email', None)
        session.pop('type', None)
        # return redirect(url_for("Login",error=error))
        return render_template('login.html', error=error)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"


@app.route("/")
def Home():

    if "email" in session:
        if session['type'] == "Mentors":
            return redirect(url_for('mentorPage'))
            

        elif session['type'] == 'Interns':
            data=db.Interns.find_one({"emailId":session['email']})
            array=[]

            for data in data['inductionPlan']['modules']:
                temp={
                    "name":"",
                    "rating":"",
                    "rkts":0,
                    "suggestions":""
                }
                if data['RKT'] == True:
                    temp['name']=data['moduleName']
                    temp['rating']=data['rating']
                    temp['rkts']=data['noOfRKTs']
                    temp['suggestions']=data['suggestions']

                elif data['RKT'] == False and 'rating' in data and data['rating'] == "Below Expectations":
                    temp['name']=data['moduleName']
                    temp['rating']=data['rating']
                    temp['rkts']=data['noOfRKTs']
                    temp['suggestions']=data['suggestions']
                else:
                    temp['name']=data['moduleName']
                    temp['rating']="RKT to happen yet"
                    temp['rkts']=0
                    temp['suggestions']="No comments"
                array.append(temp)
            return render_template('home.html', data=array)
        elif  session['type'] == "Managers":
            return redirect(url_for('managerPage'))
        elif  session['type'] == "Admin":
            return redirect(url_for('adminPage'))
        else:
            return render_template('home.html')
    else:
        return redirect(url_for('Login'))


def verifyToken(token):
    serial = Serializer(app.config['SECRET_KEY'])
    email = ""
    type = ""
    try:
        email = serial.loads(token)['emailId']
        type = serial.loads(token)['type']
    except:
        return None
    DB = db.get_collection(type)
    return DB.find_one({"emailId": email})


def getToken(data, type):

    serial = Serializer(app.config['SECRET_KEY'], expires_in=1800)
    return serial.dumps({'emailId': data['emailId'], 'type': type}).decode('utf-8')


def sendMail(data, type):
    token = getToken(data, type)

    msg = EmailMessage()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        msg['Subject'] = 'Passord Reset Link from InternTracker!'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = data['emailId']

        if 'fname' in data and 'sname' in data:
            msg.add_alternative("""\

                            <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + data['fname'] + """ """ + data['sname'] + """,</h1>
                                        <p> click on the below link to reset your password.link will expire in next 30 minutes.</p>
                                        <a href=""" + url_for('resetToken', token=token, _external=True) + """> <p>Click here to reset you password!</p></a><br><br>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                    </html>
                                    """, subtype='html')
        else:
            msg.add_alternative("""\

                            <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + data['emailId'] + """,</h1>
                                        <p> click on the below link to reset your password.link will expire in next 30 minutes.</p>
                                        <a href=""" + url_for('resetToken', token=token, _external=True) + """> <p>Click here to reset you password!</p></a><br><br>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                    </html>
                                    """, subtype='html')

        smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

        smtp.send_message(msg)

    pass


@app.route("/resetpassword", methods=['GET', 'POST'])
def resetPassword():
    if 'email' in session:
        return "<p>You are not authorized entity to access this webpage</p>"
    else:
        error = ""
        if request.method == 'POST':

            email = request.form['email']
            data = None
            type=""

            internData=db.Interns.find_one({"emailId":email})
            mentorData=db.Mentors.find_one({"emailId":email})
            managerData=db.Managers.find_one({"emailId":email})
            AdminData=db.Admin.find_one({"emailId":email})


            if internData is not None:
                data=internData
                type="Interns"
            elif mentorData is not None:
                data=mentorData
                type="Mentors"
            elif managerData is not None:
                data=managerData
                type="Managers"
            elif AdminData is not None:
                data=AdminData
                type="Admin"
            else:
                data=None


            if data is None:
                error = "User doesn't exists in database."
            else:
                sendMail(data, type)
                error = "Password Reset Email sent successfully!"

            redirect(url_for("Login"))
            return render_template("login.html", error=error)
        else:
            return render_template("resetPassword.html")


@app.route("/login", methods=['GET', 'POST'])
def Login():

    if "email" not in session:
        error = ""
        if request.method == 'POST':

            email = request.form['email']
            # type = request.form['type']
            password = request.form['password']

            user = None
            type=""
            name=""
            internData=db.Interns.find_one({"emailId":email})
            mentorData=db.Mentors.find_one({"emailId":email})
            managerData=db.Managers.find_one({"emailId":email})
            AdminData=db.Admin.find_one({"emailId":email})


            if internData is not None:
                user=internData
                type="Interns"
            elif mentorData is not None:
                user=mentorData
                type="Mentors"
            elif managerData is not None:
                user=managerData
                type="Managers"
            elif AdminData is not None:
                user=AdminData
                type="Admin"
            else:
                user=None
            
            
            if user is None:
                error = "No user exists!"
            else:
                salt = user['salt']
                if 'fname' in user and 'sname' in user:
                    name=user['fname'] + " " +user['sname']
                hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                print(user['password'],hashed,bcrypt.checkpw(password.encode('utf8'), user['password']))
                if bcrypt.checkpw(password.encode('utf8'), user['password']) == False:
                    error = "Invalid Username/Password"
                else:
                    session['email'] = request.form['email']
                    session['type'] = type
                    session['name'] = name
                    return redirect(url_for("Home"))

        return render_template("login.html", error=error)

    else:
        return redirect(url_for("Home"))


@app.route('/resetpassword/<token>', methods=['GET', 'POST'])
def resetToken(token):
    error = ""
    user = verifyToken(token)
    if user is None:
        error = "Invalid user or Token expired!"
        return render_template("/resetpassword", error=error)
    else:
        data = {
            "email": user['emailId']
        }
        return render_template("changePassword.html", user=data)


@app.route("/changePassword", methods=['GET', 'POST'])
def changePassword():
    if 'email' in session:
        return "<p>You are not authorized entity to access this webpage</p>"
    else:
        if request.method == 'POST':

            if request.form['password1'] == request.form['password2']:

                error=""
                Mentor=db.Mentors.find_one({"emailId":request.form['email']})
                Admin=db.Admin.find_one({"emailId":request.form['email']})
                Manager=db.Managers.find_one({"emailId":request.form['email']})
                Intern=db.Interns.find_one({"emailId":request.form['email']})
                password=request.form['password1']

                if Mentor is not None:
                    salt = Mentor['salt']
                    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                    try:
                        DB=db.Mentors
                        DB.update_one({"emailId":request.form['email']},{"$set":{"password":hashed}})
                        error="Password updated successfully!"
                    except:
                        error="error occurred!"
                    
                elif Admin is not None:
                    salt = Admin['salt']
                    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                    try:
                        DB=db.Admin
                        DB.update_one({"emailId":request.form['email']},{"$set":{"password":hashed}})
                        error="Password updated successfully!"
                    except:
                        error="error occurred!"
                elif Manager is not None:
                    salt = Manager['salt']
                    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                    try:
                        DB=db.Managers
                        DB.update_one({"emailId":request.form['email']},{"$set":{"password":hashed}})
                        error="Password updated successfully!"
                    except:
                        error="error occurred!"
                else:
                    
                    salt = Intern['salt']
                    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                    try:
                        DB=db.Interns
                        DB.update_one({"emailId":request.form['email']},{"$set":{"password":hashed}})
                        error="Password updated successfully!"
                    except:
                        error="error occurred!"

                return render_template("login.html",error=error)
            else:
                data = {
                    "error": "Passwords unmatched,enter again!",
                    "email": request.form['email']
                }
                return render_template("changePassword.html", user=data)

        else:
            data = {
                "email": request.form['email']
            }
            return render_template("changePassword.html", user=data)
