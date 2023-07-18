from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["JobSe"]
collection = db["jobse"]

@app.route("/")
def index():
    documents = collection.find()
    return render_template("index.html", documents=documents)

if __name__ == '__main__':
    app.run()