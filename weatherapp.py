from flask import Flask
from flask import request
import requests
from flask import render_template
from pymongo import MongoClient
app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = request.form
        client = MongoClient("mongodb://127.0.0.1:27017/")
        db = client['login']
        collection = db['login_coln']
        password_extract = collection.find_one(
            {"username": form_data['username']})
        if password_extract:
            password = password_extract['password']
            if password == form_data['password']:
                return render_template("index.html")
            else:
                return render_template('login.html')
        else:
            return render_template("signup.html")

    return render_template("login.html")


@app.route('/weather', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        form_data = request.form
        # print(form_data)
        # print(url.format(form_data['city']))
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=271d1234d3f497eed5b1d80a07b3fcd1".format(
            form_data['city'])
        resp = requests.get(url=url).json()
        # print(resp)
        city = resp['name']
        temp = resp['main']['temp']
        description = resp['weather'][0]['description']
        icon = resp['weather'][0]['icon']
        temp_deg_cel = int(temp-273.15)
        weather = {"City": city, "Temp": temp_deg_cel,"description": description, "icon": icon}
        print(temp_deg_cel)
    return render_template("temp.html", weather=weather)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        form_data = request.form
        client = MongoClient("mongodb://127.0.0.1:27017/")
        db = client['login']
        collection = db['login_coln']
        if not collection.find_one({"username": form_data['username']}):
            if form_data['password'] != form_data['ConfirmPassword']:
                return "Password Does not match"
            else:
                credentials = {
                    "username": form_data['username'], "password": form_data['password']}
                collection.insert(credentials)
                return render_template("login.html")
        else:
            return "Username already Taken"
    return render_template("signup.html")


app.run(debug=True)
