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

if __name__ == '__main__':
    app.run()