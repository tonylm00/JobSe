from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["JobSe"]
collection = db["jobse"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

'''



@app.route('/searchByCompany', methods=['POST'])
def searchByCompany():
    company = request.form.get("company")
    query = {'name': {'$regex': company, '$options': 'i'}}
    result = list(collection.find(query))
    return render_template("query.html", jobs=result)

'''
@app.template_filter('to_string')
def to_string(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

@app.route('/searchByDesignation', methods=['POST'])
def searchByDesignation():
    des = request.form.get("designation")
    query = {'designation': {'$regex': des, '$options': 'i'}}
    result = list(collection.find(query))
    return render_template("query.html", jobs=result)

@app.route('/viewJob', methods=['POST'])
def viewJob():
    work = request.form.get("work")
    result = collection.find_one({'_id': ObjectId(work)})

    return render_template("viewJob.html", job=result)

#OR tra due lavori
@app.route('/workORwork', methods=['POST'])
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

    return render_template("query.html", jobs=result)

#AND lavoro e work_type
@app.route('/workANDtype', methods=['POST'])
def workANDtype():
    work = request.form.get("work")
    type = request.form.get("type")
    print("work: ",work," type: ",type)
    query = {
        '$and': [
            {'designation': work},
            {'work_type': type}
        ]
    }
    result = list(collection.find(query))
    return render_template("query.html", jobs=result)

#work_type AND salary OR work type AND salary
@app.route('/typeANDsalaryORsame', methods=['POST'])
def typeANDsalaryORsame():
    work1 = request.form.get("work1")
    salary1 = request.form.get("salary1")
    work2 = request.form.get("work2")
    salary2 = request.form.get("salary2")

    query = {
        'or': [
            {
                '$and': [{'work_type': work1}, {'monthly_salary': {'$lt': salary1}}]
            },
            {
                '$and': [{'work_type': work2}, {'monthly_salary': {'$lt': salary2}}]
            }
        ]
    }
    print(query)
    result = list(collection.find(query))
    return render_template("query.html", jobs=result)

@app.route('/updateView')
def updateView():
    page_number = request.args.get("page")  # Get the value of the 'page' parameter
    page_number = int(page_number)

    # Calcola gli indici di inizio e fine dell'intervallo dell'array
    start_index = (page_number - 1) * 20
    end_index = start_index + 20

    start_page = max(1, page_number - 5)
    # Calcola il punto di arrivo del ciclo
    end_page = page_number + 5

    jobs = list(collection.find())  # Fetch job data from the database
    print(jobs)
    page_data = jobs[start_index:end_index]
    return render_template("updateView.html", jobs=page_data,
        current_page=page_number,
        total_pages=280,
        start_page=start_page,
        end_page=end_page)

@app.route('/updateJob/<string:job_id>', methods=['GET', 'POST'])
def updateJob(job_id):
    page_number = request.args.get("page")  # Get the value of the 'page' parameter
    if request.method == 'POST':
        try:
            job = {
                "designation": request.form.get("designation"),
                "name": request.form.get("name"),
                "involvement": request.form.get("involvement"),
                "job_details": request.form.get("job_details"),
                "industry": request.form.get("industry"),
                "level": request.form.get("level"),
                "City": request.form.get("City"),
                "State": request.form.get("State"),
                "monthly_salary": request.form.get("monthly_salary")
            }
            collection.update_one({"_id": ObjectId(job_id)}, {"$set": job})
            message = "Job announcement data successfully updated"
            page_number = int(page_number)

            # Calcola gli indici di inizio e fine dell'intervallo dell'array
            start_index = (page_number - 1) * 20
            end_index = start_index + 20

            start_page = max(1, page_number - 5)
            # Calcola il punto di arrivo del ciclo
            end_page = page_number + 5

            jobs = list(collection.find())  # Fetch job data from the database
            page_data = jobs[start_index:end_index]
            return render_template("updateView.html", message=message, jobs=page_data, current_page = page_number,
                        total_pages=280,
                        start_page=start_page,
                        end_page=end_page)
        except PyMongoError as e:
            message = "Error while updating the job ad.: " + str(e)
    else:
        job = collection.find_one({"_id": ObjectId(job_id)})  # Fetch the specific job details
        message = ""

    return render_template("update.html", job=job, message=message, current_page = page_number)

#Eliminazione offerta di lavoro
@app.route('/deleteJob/<string:job_id>', methods=['POST'])
def deleteJob(job_id):
    try:
        collection.delete_one({"_id": ObjectId(job_id)})
        message = "Job is successfully deleted"
    except PyMongoError as e:
        message = "Error while deleting job announcement" + str(e)

    page_number = request.args.get("page")  # Get the value of the 'page' parameter
    page_number = int(page_number)

    # Calcola gli indici di inizio e fine dell'intervallo dell'array
    start_index = (page_number - 1) * 20
    end_index = start_index + 20

    start_page = max(1, page_number - 5)
    # Calcola il punto di arrivo del ciclo
    end_page = page_number + 5

    jobs = list(collection.find())  # Fetch job data from the database
    page_data = jobs[start_index:end_index]
    return render_template("updateView.html", jobs=page_data,
                           message = message,
                           current_page=page_number,
                           total_pages=280,
                           start_page=start_page,
                           end_page=end_page)

@app.route('/insertJob', methods=['GET', 'POST'])
def insertJob():
    if request.method == 'POST':
        try:
            job = {
                "designation": request.form.get("designation"),
                "name": request.form.get("name"),
                "involvement": request.form.get("involvement"),
                "job_details": request.form.get("job_details"),
                "industry": request.form.get("industry"),
                "level": request.form.get("level"),
                "City": request.form.get("City"),
                "State": request.form.get("State"),
                "monthly_salary": request.form.get("monthly_salary")
            }
            collection.insert_one(job)
            message = "Annuncio di lavoro aggiunto con successo"
        except PyMongoError as e:
            message = "Errore durante l'inserimento dell'annuncio di lavoro: " + str(e)
    else:
        message = ""

    return render_template("insert.html", message=message)

@app.route('/searchById', methods=['GET', 'POST'])
def searchByID():
    work = request.args.get("searchId")
    job = collection.find_one({"_id": ObjectId(work)})
    return render_template("updateView.html", jobs = [job])

if __name__ == '__main__':
    app.run()