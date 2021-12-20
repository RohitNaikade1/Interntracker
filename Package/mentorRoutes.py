from Package import *

@app.route("/deleteMentor",methods=['POST'])
def deleteMentor():
    if request.method == 'POST':
        email=request.form['email']
        Mentor=db.Mentors
        Managers=db.Managers

        Managers.update_one({"emailId":session['email']},{"$pull":{"mentors":email}})
        Mentor.delete_one({"emailId":email})
        mentor=Mentor.find({})

        return render_template('manager.html',mentors=mentor)
    else:
        Mentor=db.Mentors
        mentor=Mentor.find({})

        return render_template('manager.html',mentors=mentor)
        
@app.route("/mentor",methods=['POST','GET'])
def mentorPage():
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
            internDB.insert_one({"emailId":intern,"password":hashed,"inductionPlan":plan,"mentor":mentor,"lastUpdate":date.today()})
            mentorDB.update_one({"emailId":mentor},{'$push':{"interns":intern}},upsert=True)

            msg = Message('Your Intern Account is created Successfully on InternTracker under Mentor ' + mentor +'.Login on InternTracker portal and check your induction plan Named '+plan['name'], sender = 'naikaderohit833@gmail.com', recipients = [intern])
            msg.body = "Your Email address is" + intern + "And Password is " + password
            mail.send(msg)
            print("email sent",msg)

            error="Intern added Successfully"
            return render_template('mentor.html',error=error)
        return render_template('mentor.html',error=error)
    else:

        Interns=db.Interns
        intern=Interns.find({})
        return render_template('mentor.html',interns=intern)