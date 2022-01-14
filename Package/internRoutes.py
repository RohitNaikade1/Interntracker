from Package import *

@app.route("/deleteIntern",methods=['POST'])
def deleteIntern():

    if "email" in session and session['type'] == "Managers" or session['type'] == "Mentors" or session['type'] == "Admin":
        if request.method == 'POST':
            email=request.form['email']
            try:
                Intern=db.Interns
                Mentors=db.Mentors
                internData=Intern.find_one({"emailId":email})
                Mentors.update_one({"emailId":internData['mentor']},{"$pull":{"interns":email}})
                Intern.delete_one({"emailId":email})
            
                intern=Intern.find({})
                data={
                        "error":"Intern deleted successfully",
                        "interns":intern,
                        "plans":[]
                    }
                plans=db.Plans.find({})
                for res in plans:
                    data['plans'].append(res['name'])
                return render_template('mentor.html',data=data)
                
            except:
                Intern=db.Interns
                intern=Intern.find({})
                data={
                        "error":"Error occurred!",
                        "interns":intern,
                        "plans":[]
                    }
                plans=db.Plans.find({})
                for res in plans:
                    data['plans'].append(res['name'])
                return render_template('mentor.html',data=data)

        else:
            Intern=db.Interns
            intern=Intern.find({})
            data={
                    "interns":intern,
                    "plans":[]
                }
            plans=db.Plans.find({})
            for res in plans:
                data['plans'].append(res['name'])
            return render_template('mentor.html',data=data)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"