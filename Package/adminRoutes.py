from Package import *

# Admin Account
# Admin=db.Admin
# AdminEmail="rohit.naikade@gslab.com"
# AdminPassword="Admin@123"

# getAdmin=Admin.find_one({"emailId":AdminEmail})

# if getAdmin is None:
#     salt=bcrypt.gensalt()
#     hashpass=bcrypt.hashpw(AdminPassword.encode('utf-8'),salt)
#     print(AdminPassword,salt,hashpass)

#     Admin.insert_one({"emailId":AdminEmail,"password":hashpass})


@app.route("/admin", methods=['POST', 'GET'])
def adminPage():

    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        Manager = db.Managers
        manager = Manager.find_one({"emailId": email})
        if manager:
            error = "Manager already exists"
        else:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf8'), salt)
            Manager.insert_one({"emailId": email, "password": hashed})

            msg = EmailMessage()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                msg['Subject'] = 'Your Manager Account is created Successfully on InternTracker'
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = email
                msg.add_alternative("""\

                            <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + email + """,</h1>
                                        <p> Your Email address is """ + email + """ And Password is """ + password + """</p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                    </html>
                                    """, subtype='html')

                smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

                smtp.send_message(msg)
            error = "Manager added Successfully"
            return render_template('admin.html', error=error)
        return render_template('admin.html', error=error)
    else:
        Managers = db.Managers
        manager = Managers.find({})

        return render_template('admin.html', managers=manager)
