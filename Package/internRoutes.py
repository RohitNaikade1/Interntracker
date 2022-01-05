from Package import *

@app.route("/deleteIntern",methods=['POST'])
def deleteIntern():

    if "email" in session and session['type'] == "Managers" or session['type'] == "Mentors" or session['type'] == "Admin":
        if request.method == 'POST':
            email=request.form['email']
            try:
                Intern=db.Interns
                Mentors=db.Mentors
                Mentors.update_one({"emailId":session['email']},{"$pull":{"interns":email}})
                Intern.delete_one({"emailId":email})
            
                intern=Intern.find({})
                data={
                        "error":"Intern deleted successfully",
                        "interns":intern
                    }
                return render_template('mentor.html',interns=data)
                
            except:
                Intern=db.Interns
                intern=Intern.find({})
                data={
                        "error":"Error occurred!",
                        "interns":intern
                    }
                return render_template('mentor.html',interns=data)

        else:
            Intern=db.Interns
            intern=Intern.find({})

            return render_template('admin.html',interns=intern)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"