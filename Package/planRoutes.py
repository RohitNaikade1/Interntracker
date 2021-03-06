from Package import *


@app.route("/deletePlan", methods=['POST', 'GET'])
def deletePlan():

    if "email" in session and session['type'] != "Interns":
        error = ""

        if request.method == 'POST':
            try:
                Plans = db.Plans
                Plans.delete_one({"name": request.form['name']})
                error = "Plan deleted successfully!"
            except:
                error = "Error occurred!"

        Plans = db.Plans
        plans = Plans.find({})
        data = []

        for cursor in plans:
            res = {
                'name': "",
                'count': 0,
                "id":""
            }
            res['name'] = cursor['name']
            res['count'] = len(cursor['modules'])
            res['id'] = cursor['_id']
            data.append(res)
        records = {
            "error": error,
            "plans": data
        }
        return render_template("plans.html", data=records)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"


@app.route("/viewPlan", methods=['POST', 'GET'])
def viewPlan():

    if "email" in session:
        data = {}
        if session['type'] == 'Interns':
            Interns = db.Interns
            data = Interns.find_one({"emailId": session['email']})
            data = data['inductionPlan']
        else:
            name = request.form['name']
            Plans = db.Plans
            data = Plans.find_one({"name": name})

        return render_template("viewPlans.html", data=data)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"


@app.route("/exportPlan", methods=['GET', 'POST'])
def exportPlan():

    if "email" in session:
        data = {}
        if session['type'] == 'Interns':
            Interns = db.Interns
            data = Interns.find_one({"emailId": session['email']})
            data = data['inductionPlan']
        else:
            Interns = db.Interns
            data = Interns.find_one({"emailId": request.form['email']})
            data = data['inductionPlan']

        return render_template("exportPlans.html", data=data)
    else:
        return "<p>You are not authorized entity to access this webpage</p>"


@app.route("/plans", methods=['POST', 'GET'])
def plans():

    if "email" in session:
        if request.method == 'POST':
            file = request.files['file']
            name = request.form['planName']

            try:
                Plans = db.Plans
                plans = Plans.find_one({"name": name})

                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], file.filename))
                excel_file = "Package/static/profiles/"+file.filename
                file = pd.ExcelFile(excel_file)
                length = len(file.sheet_names)

                if plans is None:
                    modules = []

                    Plans.insert_one({"name": name, "modules": []})
                    for i in range(0, length):
                        sheet = pd.read_excel(excel_file, sheet_name=i)
                        moduleName = ""
                        for i in sheet['skill module']:
                            if isinstance(i, str):
                                moduleName = i

                        subModules = []
                        subModule = []
                        Assignments = []
                        PDs = []
                        for i in sheet['PDs']:
                            if isinstance(i, float):
                                PDs.append(i)

                        for i in sheet['sub module']:
                            if isinstance(i, str):
                                subModule.append(i)

                        for i in range(0, len(PDs)):
                            temp = {
                                "name": "",
                                "PD": 0,
                                "status": "Pending",
                                "startDate": "",
                                "endDate": ""
                            }
                            temp['name'] = subModule[i]
                            temp['PD'] = PDs[i]

                            subModules.append(temp)

                        res = {
                            "moduleName": moduleName,
                            "subModules": subModules,
                            "RKT": False,
                            "noOfRKTs":0,
                            "RKTHistory":[]
                        }

                        Plans.find_one_and_update(
                            {"name": name}, {"$push": {"modules": res}})
                else:
                    Plans.find_one_and_update(
                        {"name": name}, {"$set": {"modules": []}})
                    for i in range(0, length):
                        sheet = pd.read_excel(excel_file, sheet_name=i)
                        moduleName = ""
                        for i in sheet['skill module']:
                            if isinstance(i, str):
                                moduleName = i

                        subModules = []
                        subModule = []
                        Assignments = []
                        PDs = []
                        for i in sheet['PDs']:
                            if isinstance(i, float):
                                PDs.append(i)

                        for i in sheet['sub module']:
                            if isinstance(i, str):
                                subModule.append(i)

                        for i in range(0, len(PDs)):
                            temp = {
                                "name": "",
                                "PD": 0,
                                "status": "Pending",
                                "startDate": "",
                                "endDate": ""
                            }
                            temp['name'] = subModule[i]
                            temp['PD'] = PDs[i]

                            subModules.append(temp)

                        res = {
                            "moduleName": moduleName,
                            "subModules": subModules,
                            "RKT": False,
                            "noOfRKTs":0,
                            "RKTHistory":[]
                        }

                        Plans.find_one_and_update(
                            {"name": name}, {"$push": {"modules": res}})

                os.remove(excel_file)

                plans = Plans.find({})
                data = []

                for cursor in plans:
                    res = {
                        "name": "",
                        "count": 0,
                        "id": ""
                    }
                    res['name'] = cursor['name']
                    res['count'] = len(cursor['modules'])
                    res['id'] = cursor['_id']
                    data.append(res)
                records = {
                    "error": "Plan Activated Successfully",
                    "plans": data
                }
                return render_template("plans.html", data=records)
            except:
                plans = Plans.find({})
                data = []

                for cursor in plans:
                    res = {
                        "name": "",
                        "count": 0,
                        "id": ""
                    }
                    res['name'] = cursor['name']
                    res['count'] = len(cursor['modules'])
                    res['id'] = cursor['_id']
                    data.append(res)

                records = {
                    "error": "Error occurred!",
                    "plans": data
                }
                return render_template("plans.html", data=records)
        else:
            Plans = db.Plans
            plans = Plans.find({})
            data = []

            for cursor in plans:
                res = {
                    'name': "",
                    'count': 0,
                    "id": ""
                }
                res['name'] = cursor['name']
                res['count'] = len(cursor['modules'])
                res['id'] = cursor['_id']
                data.append(res)
            records = {
                "plans": data
            }
            return render_template("plans.html", data=records)

    else:
        return "<p>You are not authorized entity to access this webpage</p>"


@app.route("/updateStatus", methods=['POST'])
def updateStatus():

    if "email" in session:
        Interns = db.Interns

        data = Interns.find_one(
            {"emailId": session['email'], "inductionPlan.modules.subModules.name": request.form['submodule']})

        # induction=data['inductionPlan']
        for rec in data['inductionPlan']['modules']:
            if rec['moduleName'] == request.form['module']:
                for d in rec['subModules']:
                    if d['name'] == request.form['submodule']:
                        d['status'] = request.form['curr']
                        d['startDate'] = request.form['start']
                        d['endDate'] = request.form['end']


        Interns.update_one({"emailId": session['email']}, {"$set": {
                           "inductionPlan": data['inductionPlan'], "lastUpdate": request.form['end']}})

        return redirect(url_for("exportPlan"))
    else:
        return "<p>You are not authorized entity to access this webpage</p>"
