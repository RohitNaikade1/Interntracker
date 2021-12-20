from Package import *

@app.route("/profile",methods=['GET','POST'])
def profile():
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

        print(fname,sname,email,mobNo,address,education,country,state)
        print(session['type'])

        collection=db.get_collection(session['type'])
        collection.update_one({"emailId":email},{"$set":{"fname":fname,"sname":sname,"mobNo":mobNo,"city":city,"address":address,"education":education,"country":country,"state":state}})
        data=collection.find_one({"emailId":email})
        return render_template("profile.html",data=data)
    else:
        collection=db.get_collection(session['type'])
        data=collection.find_one({"emailId":session['email']})
        return render_template('profile.html',data=data)

@app.route("/profilepic",methods=['POST'])
def profilepic():

    msg=""
    if request.method== 'POST':

        file = request.files['file']
        filename = secure_filename(file.filename)
    
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            now = datetime.now()
            date_time = now.strftime("%m_%d_%Y, %H:%M:%S")
            
            old_name = r"static/profiles/"+filename
            new_name = r"static/profiles/"+date_time+filename

            os.rename(old_name,new_name)
            print(date_time+filename)

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
    