from logging import Manager
from pymongo import MongoClient, collection
import urllib.parse
from flask import *
import bcrypt
from flask_mail import Mail,Message
from flask_pymongo import PyMongo
app=Flask(__name__)
from werkzeug.utils import secure_filename
import os
import pandas as pd

from datetime import datetime

app.config['SECRET_KEY']='rohit'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rohit.naikade@gslab.com'
app.config['MAIL_PASSWORD'] = 'vgshfwkiyxjrnuyp'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
UPLOAD_FOLDER = 'static/profiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
mail = Mail(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# client=MongoClient("mongodb+srv://GSLab:"+urllib.parse.quote("gslab@123")+"@cluster0.v2mwo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/InterTracker")
db = mongodb_client.db



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
            mentorDB.insert_one({"emailId":mentor,"password":hashed})
            managerDB.update_one({"emailId":manager},{'$push':{"mentors":mentor}},upsert=True)

            msg = Message('Your Mentor Account is created Successfully on InternTracker under Manager ' + manager, sender = 'naikaderohit833@gmail.com', recipients = [mentor])
            msg.body = "Your Email address is" + mentor + "And Password is " + password
            mail.send(msg)
            print("email sent",msg)

            error="Mentor added Successfully"
            return render_template('manager.html',error=error)
        return render_template('manager.html',error=error)
    else:
        Mentors=db.Mentors
        mentor=Mentors.find({})
        return render_template('manager.html',mentors=mentor)
    
@app.route("/plans",methods=['POST','GET'])
def plans():
    if request.method == 'POST':
        file=request.files['file']
        name=request.form['planName']

        Plans=db.Plans
        plans=Plans.find_one({"name":name})

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        excel_file = "static/profiles/"+file.filename
        file = pd.ExcelFile(excel_file)
        length=len(file.sheet_names)

        if plans is None:
            print("No record")
            modules=[]
            

            Plans.insert_one({"name":name,"modules":[]})
            for i in range(0,length):
                sheet=pd.read_excel(excel_file,sheet_name=i)
                moduleName=""
                for i in sheet['skill module']:
                    if isinstance(i,str):
                        moduleName=i

                subModules=[]
                subModule=[]
                Assignments=[]
                PDs=[]
                for i in sheet['PDs']:
                    if isinstance(i,float):
                        PDs.append(i)
    
                for i in sheet['Assignments']:
                    if isinstance(i,str):
                        Assignments.append(i)
    
                for i in sheet['sub module']:
                    if isinstance(i,str):
                        subModule.append(i)

                for i in range(0,len(PDs)):
                    temp={
                        "name":"",
                        "PD":0
                    }
                    temp['name']=subModule[i]
                    temp['PD']=PDs[i]
                    
                    subModules.append(temp)

                res={
                    "moduleName":moduleName,
                    "subModules":subModules,
                    "Assignments":Assignments
                }
                
                Plans.find_one_and_update({"name":name},{"$push":{"modules":res}})
        else:
            for i in range(0,length):
                sheet=pd.read_excel(excel_file,sheet_name=i)
                moduleName=""
                for i in sheet['skill module']:
                    if isinstance(i,str):
                        moduleName=i

                subModules=[]
                subModule=[]
                Assignments=[]
                PDs=[]
                for i in sheet['PDs']:
                    if isinstance(i,float):
                        PDs.append(i)
    
                for i in sheet['Assignments']:
                    if isinstance(i,str):
                        Assignments.append(i)
    
                for i in sheet['sub module']:
                    if isinstance(i,str):
                        subModule.append(i)

                for i in range(0,len(PDs)):
                    temp={
                        "name":"",
                        "PD":0
                    }
                    temp['name']=subModule[i]
                    temp['PD']=PDs[i]
                    
                    subModules.append(temp)

                res={
                    "moduleName":moduleName,
                    "subModules":subModules,
                    "Assignments":Assignments
                }
                
                Plans.find_one_and_update({"name":name},{"$push":{"modules":res}})
        
        
        os.remove(excel_file)

        plans=Plans.find({})
        data=[]

        for cursor in plans:
            res={
                "name":"",
                "count":0
            }
            res['name']=cursor.name
            res['count']=len(cursor.modules)
            data.append(res)
        return render_template("plans.html",data=data)
    else:
        Plans=db.Plans
        plans=Plans.find({})
        data=[]

        for cursor in plans:
            res={
                'name':"",
                'count':0
            }
            res['name']=cursor['name']
            res['count']=len(cursor['modules'])
            data.append(res)
        return render_template("plans.html",data=data)

@app.route("/mentor",methods=['POST','GET'])
def mentorPage():
    error=""
    if request.method=='POST':
        intern=request.form['intern']
        mentor=request.form['mentor']
        password=request.form['password']

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
            internDB.insert_one({"emailId":intern,"password":hashed})
            mentorDB.update_one({"emailId":mentor},{'$push':{"interns":intern}},upsert=True)

            msg = Message('Your Intern Account is created Successfully on InternTracker under Mentor ' + mentor, sender = 'naikaderohit833@gmail.com', recipients = [intern])
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

@app.route("/")
def Home():
    return render_template('home.html')

@app.route("/login",methods=['GET','POST'])
def Login():

    if request.method=='POST':

        error=""
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
    if session.get('email') == True:
        return redirect(url_for('Home'))
    else:
        return render_template('login.html')

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
    
@app.route("/delete")
def delete():
    print(request.form['delete'])
    return render_template("/")
@app.route("/logout")
def Logout():
    error="You have signed out successfully!"
    session.pop('email',None)
    session.pop('type',None)
    return render_template('login.html',error=error)

if __name__ == '__main__':
    app.run(debug=True,port=5007)