from Package import *



@app.route("/leaves",methods=['POST','GET'])
def leaves():

    if request.method == 'POST':
        date=request.form['date']
        type=request.form['type']
        reason=request.form['reason']

        Interns=db.Interns
        intern=Interns.find_one({"emailId":session['email']})
        msg = Message("Leave application from "+ session['email'], sender = 'naikaderohit833@gmail.com', recipients = [intern['mentor']])
        msg.body = "You have received a leave application from " + session['email'] +".Login and Approve/Reject the same and notify him/her about Remark."
        mail.send(msg)
        add={
            "date":date,
            "type":type,
            "reason":reason,
            "visible":True
        }
        Interns.update_one({"emailId":session['email']},{"$push":{"leaves":add}})

        data=Interns.find_one({"emailId":session['email']})
        if "leaves" in data:
            return render_template("leaves.html",data=data['leaves'])
        else:
            return render_template("leaves.html",data=[])
    else:
        Interns=db.Interns
        data=Interns.find_one({"emailId":session['email']})
        if "leaves" in data:
            return render_template("leaves.html",data=data['leaves'])
        else:
            return render_template("leaves.html",data=[])

@app.route("/leaveActions",methods=['POST'])
def leaveActions():
    name=request.form['name']
    date=request.form['key']
    email=request.form['email']
    Interns=db.Interns
    Interns.update_one({"emailId":email,"leaves.date":date,"leaves.visible":True},{"$set":{"leaves.$.remarks":name,"leaves.$.visible":False}})

    msg = Message("Status of Leave Application!", sender = 'naikaderohit833@gmail.com', recipients = [email])
    msg.body = "Your Mentor have reacted on your leave application.your application remark is "+name
    mail.send(msg)

    return redirect(url_for('Home'))