from sys import modules
from Package import *

@app.route("/renderFeedback",methods=['GET','POST'])
def renderFeedback():
    
    if "email" in session and session['type'] == "Mentors":
        data=request.form['email']
        return render_template("feedback.html",data=data)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"

@app.route("/feedback", methods=['GET', 'POST'])
def Feedback():
    if "email" in session and session['type'] == "Mentors":
        error=""
        if request.method == 'POST':

            Interns = db.Interns
            data = Interns.find_one({"emailId": request.form['email']})

            if request.form['rating'] == 'Below Expectations':

                if request.form['deadline'] == "":
                    error="please select deadline!"
                    return render_template("feedback.html",error=error)

                for module in data['inductionPlan']['modules']:
                    if module['moduleName'] == request.form['topic']:
                        module['deadline'] = request.form['deadline']
                        module['RKT'] = False
                        module['rating'] = request.form['rating']
                        
                Interns.update_one({"emailId": request.form['email']}, {
                               "$set": {"inductionPlan": data['inductionPlan']}})

                to = [data['emailId']]
                msg = EmailMessage()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                    msg['Subject'] = "Mentor's Feedback"
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = ','.join(to)
                    msg.set_content("Mentor's Feedback")

                    if 'fname' in data and 'sname' in data:
                        msg.add_alternative("""\

                        <!DOCTYPE html>
                            <body>
                                <h1> Hello """ + data['fname'] + """ """ + data['sname'] + """,</h1>
                                    <p> You haven't satisfactorily performed during an RKT on topic <b>""" + request.form['topic'] + """</b>.your mentor have set a deadline for same topic revision on """ + request.form['deadline'] + """.prepare well and schedule RKT on """ + request.form['deadline']+""" </p>
                                    <p>All the best!</p>
                                    <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                            </body>
                        </html>
                            """, subtype='html')

                    else:
                        msg.add_alternative("""\

                        <!DOCTYPE html>
                            <body>
                                <h1> Hello """ + data['emailId'] + """,</h1>
                                    <p> You haven't satisfactorily performed during an RKT on topic <b>""" + request.form['topic'] + """</b>.your mentor have set a deadline for same topic revision on """ + request.form['deadline'] + """.prepare well and schedule RKT on """ + request.form['deadline']+""" </p>
                                    <p>All the best!</p>
                                    <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                            </body>
                        </html>
                            """, subtype='html')

                    smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

                    smtp.send_message(msg)

                    error="Feedback submitted successfully!"
                    return render_template("feedback.html",error=error)

            else:

                for module in data['inductionPlan']['modules']:
                    if module['moduleName'] == request.form['topic']:
                        module['deadline'] = ""
                        module['RKT'] = True
                        module['rating'] = request.form['rating']

                Interns.update_one({"emailId": request.form['email']}, {
                               "$set": {"inductionPlan": data['inductionPlan']}})

                to = [data['emailId']]
                msg = EmailMessage()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                    msg['Subject'] = "Mentor's Feedback"
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = ','.join(to)
                    msg.set_content("Mentor's Feedback")

                    if 'fname' in data and 'sname' in data:
                        msg.add_alternative("""\

                        <!DOCTYPE html>
                            <body>
                                <h1> Hello """ + data['fname'] + """ """ + data['sname'] + """,</h1>
                                    <p> You haven satisfactorily performed during an RKT on topic <b>""" + request.form['topic'] + """</b>.your mentor have submitted a measure <b>""" + request.form['rating'] + """</b>.you can continue with your next topic.</p>
                                    <p>Mentor's Suggestions:</p>

                                <blockquote >
                                """+ request.form['suggestions']+"""
                                </blockquote>
                                <p>All the best!</p>
                                <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                            </body>
                        </html>
                            """, subtype='html')

                    else:
                        msg.add_alternative("""\

                        <!DOCTYPE html>
                            <body>
                                <h1> Hello """ + data['emailId'] + """,</h1>
                                <p> You haven satisfactorily performed during an RKT on topic <b>""" + request.form['topic'] + """</b>.your mentor have submitted a measure <b>""" + request.form['rating'] + """</b>.you can continue with your next topic.</p>
                                <p>Mentor's Suggestions:</p>

                                <blockquote>
                                """+ request.form['suggestions']+"""
                                </blockquote>
                                <p>All the best!</p>
                                <img style="margin-top:50px;" src="https://i.pinimg.com/600x315/43/e2/e7/43e2e73f1c55e01ebf043b8e264c9424.jpg"></img>
                            </body>
                        </html>
                            """, subtype='html')

                    smtp.login(EMAIL_ADDRESS, MAIL_PASSWORD)

                    smtp.send_message(msg)
                    error="Feedback submitted successfully!"
                    return render_template("feedback.html",error=error)
        else:
            return render_template("feedback.html")

    else:
        return "<p>You are not authorized entity to access this webpage</p>"