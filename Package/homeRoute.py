from Package import *

@app.route("/logout")
def Logout():

    if "email" in session:
        error="You have signed out successfully!"
        session.pop('email',None)
        session.pop('type',None)
        # return redirect(url_for("Login",error=error))
        return render_template('login.html',error=error)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"
    
@app.route("/")
def Home():

    if "email" in session:
        if session['type'] == "Mentors":
            Interns=db.Interns
            data=[]
            interns=Interns.find({"mentor":session['email']})
        
            for intern in interns:
                if "leaves" in intern:
                    for rec in intern["leaves"]:
                        rec.update({'emailId':intern['emailId']})
                        data.append(rec)
            return render_template('home.html',data=data)
        else:
            return render_template('home.html')
    else:
        return "<p>You are not authorized entity to access this webpage</p>"

@app.route("/login",methods=['GET','POST'])
def Login():

    if "email" not in session:
        error=""
        if request.method=='POST':

            
            email=request.form['email']
            type=request.form['type']
            password=request.form['password']

            cursor=db.get_collection(type)
            user=cursor.find_one({"emailId":email})

            if user is None:
                error="No user exists!"
            else:
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                print("reached")
                if bcrypt.checkpw(hashed, user['password']):
                    error="Invalid Username/Password"
                else:
                    session['email'] = request.form['email']
                    session['type'] = request.form['type']
                    return redirect(url_for("Home"))
       
        return render_template("login.html",error=error)
        
    else:
        return redirect(url_for("Home"))