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
            Interns = db.Interns
            data = []
            interns = Interns.find({"mentor": session['email']})

            for intern in interns:
                if "leaves" in intern:
                    for rec in intern["leaves"]:
                        rec.update({'emailId': intern['emailId']})
                        data.append(rec)
            return render_template('home.html', data=data)
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
                                        <p> """ + url_for('resetToken', token=token, _external=True) + """</p>
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
            type = request.form['type']

            DB = db.get_collection(type)

            data = DB.find_one({"emailId": email})

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
            type = request.form['type']
            password = request.form['password']

            cursor = db.get_collection(type)
            user = cursor.find_one({"emailId": email})

            if user is None:
                error = "No user exists!"
            else:
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                print("reached")
                if bcrypt.checkpw(hashed, user['password']):
                    error = "Invalid Username/Password"
                else:
                    session['email'] = request.form['email']
                    session['type'] = request.form['type']
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
                Manager=db.Manager.find_one({"emailId":request.form['email']})
                password=request.form['password1']

                if Mentor is not None:
                    salt = bcrypt.gensalt()
                    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                    try:
                        DB=db.Mentors
                        DB.update_one({"emailId":request.form['email']},{"$set":{"password":hashed}})
                        error="Password updated successfully!"
                    except:
                        error="error occurred!"
                    
                elif Admin is not None:
                    salt = bcrypt.gensalt()
                    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                    try:
                        DB=db.Admin
                        DB.update_one({"emailId":request.form['email']},{"$set":{"password":hashed}})
                        error="Password updated successfully!"
                    except:
                        error="error occurred!"
                elif Manager is not None:
                    salt = bcrypt.gensalt()
                    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                    try:
                        DB=db.Managers
                        DB.update_one({"emailId":request.form['email']},{"$set":{"password":hashed}})
                        error="Password updated successfully!"
                    except:
                        error="error occurred!"
                else:
                    salt = bcrypt.gensalt()
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
