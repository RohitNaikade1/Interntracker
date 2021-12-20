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

@app.route("/admin",methods=['POST','GET'])
def adminPage():

    
    error=""
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        Manager=db.Managers
        manager=Manager.find_one({"emailId":email})
        if manager:
            error="Manager already exists"
        else:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf8'), salt)
            Manager.insert_one({"emailId":email,"password":hashed})

            msg = Message('Your Manager Account is created Successfully on InternTracker', sender = 'naikaderohit833@gmail.com', recipients = [email])
            msg.body = "Your Email address is" + email + "And Password is " + password
            mail.send(msg)
            print("email sent",msg)

            error="Manager added Successfully"
            return render_template('admin.html',error=error)
        return render_template('admin.html',error=error)
    else:
        Managers=db.Managers
        manager=Managers.find({})

        return render_template('admin.html',managers=manager)