from Package import *

import datetime


@app.route("/report", methods=['GET', 'POST'])
def Report():

    if "email" in session:
        data = db.Interns.find_one({"emailId": request.form['email']})
        array = []
        cnt=0
        for data in data['inductionPlan']['modules']:
                temp = {
                    "name": "",
                    "rating": "",
                    "rkts": 0,
                    "status":"Incomplete",
                    "suggestions": ""
                }
                if data['RKT'] == True:
                    temp['name'] = data['moduleName']
                    temp['rating'] = data['rating']
                    temp['status'] = "Completed"
                    temp['rkts'] = data['noOfRKTs']
                    temp['History'] = data['RKTHistory']
                    temp['suggestions'] = data['suggestions']
                    temp['id']=cnt+1
                    cnt=cnt+1

                elif data['RKT'] == False and 'rating' in data and data['rating'] == "Below Expectations":
                    temp['name'] = data['moduleName']
                    temp['rating'] = data['rating']
                    temp['rkts'] = data['noOfRKTs']
                    temp['History'] = data['RKTHistory']
                    temp['suggestions'] = data['suggestions']
                    temp['id']=cnt+1
                    cnt=cnt+1
                else:
                    temp['name'] = data['moduleName']
                    temp['rating'] = "RKT to happen yet"
                    temp['rkts'] = 0
                    temp['History'] = data['RKTHistory']
                    temp['suggestions'] = "No comments"
                    temp['id']=cnt+1
                    cnt=cnt+1
                array.append(temp)
        return render_template('report.html', data=array)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"
