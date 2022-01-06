from Package import *

import datetime

@app.route("/profile",methods=['GET','POST'])
def profile():

    if "email" in session:
        if request.method == 'POST':
            fname=request.form['fname']
            sname=request.form['sname']
            email=request.form['email']
            mobNo=request.form['mobNo']
            address=request.form['address']
            education=request.form['education']
            country=request.form['country']
            state=request.form['state']
            city=request.form['city']

            if session['type'] == 'Managers' or session['type'] == 'Mentors':
                collection=db.get_collection(session['type'])
            

                if request.form['type'] == "Once in a week":
                    today = datetime.date.today()
                    collection.update_one({"emailId":email},{"$set":{"nextDate":str(today + datetime.timedelta(days=-today.weekday(), weeks=1)),"notifications":request.form['type'],"fname":fname,"sname":sname,"mobNo":mobNo,"city":city,"address":address,"education":education,"country":country,"state":state}})
                else:
                    today = datetime.date.today()
                    collection.update_one({"emailId":email},{"$set":{"nextDate":str(today + datetime.timedelta(days=-today.weekday(), weeks=2)),"notifications":request.form['type'],"fname":fname,"sname":sname,"mobNo":mobNo,"city":city,"address":address,"education":education,"country":country,"state":state}})

            
            else:
                collection=db.get_collection(session['type'])
                collection.update_one({"emailId":email},{"$set":{"fname":fname,"sname":sname,"mobNo":mobNo,"city":city,"address":address,"education":education,"country":country,"state":state}})
        
            data=collection.find_one({"emailId":email})
            return render_template("profile.html",data=data)
        else:
            collection=db.get_collection(session['type'])
            data=collection.find_one({"emailId":session['email']})
            return render_template('profile.html',data=data)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"

@app.route("/profilepic",methods=['POST'])
def profilepic():

    if "email" in session:
        msg=""
        if request.method== 'POST':

            file = request.files['file']
            filename = secure_filename(file.filename)
    
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                now = datetime.datetime.now()
                date_time = now.strftime("%m_%d_%Y, %H:%M:%S")
            
                old_name = r"static/profiles/"+filename
                new_name = r"static/profiles/"+date_time+filename

                os.rename(old_name,new_name)

                collection=db.get_collection(session['type'])
                user=collection.find_one({"emailId":session['email']})

                if user.get("profile") is not None:
                    os.remove(user['profile'])
                    name="static/profiles/"+date_time+filename
                    url=os.environ.get("host")+"static/profiles/"+date_time+filename
                    collection.update_one({"emailId":session['email']},{"$set":{"profile":name,"url":url}})
                else:
                    name="static/profiles/"+date_time+filename
                    url=os.environ.get("host")+"static/profiles/"+date_time+filename
                    collection.update_one({"emailId":session['email']},{"$set":{"profile":name,"url":url}})

                return redirect('/profile')
            else:
                flash('Invalid Uplaod only  png, jpg, jpeg') 
                return redirect('/')
    else:
        return "<p>You are not authorized entity to access this webpage</p>"
    