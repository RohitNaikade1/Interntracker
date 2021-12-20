from Package import *

@app.route("/deleteIntern",methods=['POST'])
def deleteIntern():
    if request.method == 'POST':
        email=request.form['email']
        Intern=db.Interns
        Mentors=db.Mentors
        Mentors.update_one({"emailId":session['email']},{"$pull":{"interns":email}})
        Intern.delete_one({"emailId":email})
        intern=Intern.find({})

        return render_template('mentor.html',interns=intern)
    else:
        Intern=db.Interns
        intern=Intern.find({})

        return render_template('admin.html',interns=intern)