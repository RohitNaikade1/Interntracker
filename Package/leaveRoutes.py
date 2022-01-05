from Package import *



@app.route("/leaves",methods=['POST','GET'])
def leaves():

    if "email" in session and session['type'] == "Interns":
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
    else:
        return "<p>You are not authorized entity to access this webpage</p>"

@app.route("/leaveActions",methods=['POST'])
def leaveActions():

    if "email" in session and session['type'] == "Mentors":
        name=request.form['name']
        date=request.form['key']
        email=request.form['email']
        Interns=db.Interns
        Interns.update_one({"emailId":email,"leaves.date":date,"leaves.visible":True},{"$set":{"leaves.$.remarks":name,"leaves.$.visible":False}})

        msg = EmailMessage()

        intern=Interns.find_one({"emailId":email})
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

            msg['Subject'] = "Status of Leave Application!"
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = intern['emailId']

            if "fname" in intern and "sname" in intern:
                msg.add_alternative("""\

                            <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + intern['fname'] + """ """ + intern['sname'] + """,</h1>
                                        <p>Your Mentor have reacted on your leave application</p>
                                        <p> your application remark is <b>""" + name + """</b></p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                    </html>
                                    """, subtype='html')
            else:
                msg.add_alternative("""\

                            <!DOCTYPE html>
                                    <body>
                                        <h1> Hello """ + intern['emailId'] + """,</h1>
                                        <p>Your Mentor have reacted on your leave application</p>
                                        <p> your application remark is <b>""" + name + """</b></p>
                                        <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                                    </body>
                                    </html>
                                    """, subtype='html')
            smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

            smtp.send_message(msg)
        return redirect(url_for('Home'))
    else:
        return "<p>You are not authorized entity to access this webpage</p>"