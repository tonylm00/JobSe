from bson import ObjectId
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["JobSe"]
collection = db["jobse"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/viewAll')
def viewAll():
    all = collection.find()
    return render_template("viewAll.html", documents=all)

@app.route('/searchByCompany', methods=['POST'])
def searchByCompany():
    company = request.form.get("company")
    query = {'name': {'$regex': company, '$options': 'i'}}
    result = list(collection.find(query))
    return render_template("searchByCompany.html", documents=result)

@app.route('/viewJob', methods=['POST'])
def viewJob():
    work = request.form.get("work")
    result = collection.find_one({'_id': ObjectId(work)})

    return render_template("viewJob.html", job=result)

#OR tra due lavori
@app.route('/viewJob', methods=['POST'])
def workORwork():
    work1 = request.form.get("work1")
    work2 = request.form.get("work2")

    query = {
        '$or': [
            {'designation': work1},
            {'designation': work2}
        ]
    }
    result = list(collection.find(query))

    return render_template("viewJob.html", jobs=result)

#AND lavoro e work_type
@app.route('/viewJob', methods=['POST'])
def workANDtype():
    work = request.form.get("work")
    type = request.form.get("type")

    query = {
        '$and': [
            {'designation': work},
            {'work_type': type}
        ]
    }
    result = list(collection.find(query))
    return render_template("viewJob.html", jobs=result)

#work_type AND salary OR work type AND salary
@app.route('/viewJob', methods=['POST'])
def workSalaryANDworkType():
    work1 = request.form.get("work1")
    salary1 = request.form.get("salary")
    work2 = request.form.get("work2")
    salary2 = request.form.get("salary")

    query = {
        'or': [
            {
                '$and': [{'designation': work1}, {'salary': salary1}]
            },
            {
                '$and': [{'designation': work2}, {'salary': salary2}]
            }
        ]
    }

    result = list(collection.find(query))
    return render_template("viewJob.html", jobs=result)

#Modifica offerta di lavoro
@app.route('/updateJob', methods=['POST'])
def updateJob():
    id = request.form.get("id")

    document = {'$set': {
        "designation": request.form.get("designation"),
        "name": request.form.get("name"),
        "work_type": request.form.get("work_type"),
        "involvement": request.form.get("involvement"),
        "job_details": request.form.get("job_details"),
        "level": request.form.get("level"),
    }
    }

    result = collection.update_one({'_id': ObjectId(id)}, document)

    if result.modified_count > 0:
        message = "Job updated successfully."
    else:
        message = "No job found matching the given query."

    return render_template("update.html", jobs=result, message=message)


#Eliminazione offerta di lavoro
@app.route('/deleteJob', methods=['POST'])
def deleteJob():

    id = ObjectId(request.form.get("id"))
    result = collection.delete_one({'_id': id})

    if result.deleted_count > 0:
        message = "Job deleted successfully."
    else:
        message = "No job found matching the given ID."

    return render_template("delete.html", message=message)


if __name__ == '__main__':
    app.run()