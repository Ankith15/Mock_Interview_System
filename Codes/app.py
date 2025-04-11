from flask import Flask, render_template

app = Flask(__name__)

jobs = [
    {'title':"Data Analyst","Location":"Bangalore","Company":"TVS","url":"https://stackoverflow.com/questions/48010748/how-to-install-the-os-module"},
    {'title':"data manager","Location":"Bangalore","Company":"TCS","url":"https://stackoverflow.com/questions/48010748/how-to-install-the-os-module"}
]

@app.route("/")
def home():
    return render_template("jobs.html",jobs=jobs)


if __name__ =="__main__":
    app.run(debug=True)