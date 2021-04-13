import json
import os
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)
ms = ""

with open('data.json', 'r') as file:
    data = json.load(file)

with open('dataa.json', 'r') as file2:
    dataa = json.load(file2)


def startup():
    if not os.path.exists("user_data.json"):
        with open("user_data.json", "w") as file1:
            json.dump([], file1)
    if not os.path.exists("logged.json"):
        with open("logged.json", "w") as file2:
            json.dump([False, "Login"], file2)
    if not os.path.exists("data.json"):
        with open("logged.json", "w") as file3:
            json.dump([], file3)
    with open("logged.json", "r") as file4:
        logged = json.load(file4)

    with open('dataa.json', 'w') as file5:
        dataa.clear()
        json.dump(dataa, file5)
    logout()
    return logged[0], logged[1]


def check_login(data, username, password):
    for i in data:
        if i["username"] == username and i["password"] == password:
            return True
    return False


def change_log_status():
    with open("logged.json", "r") as file1:
        logged = json.load(file1)
    global logged_in, log_status
    logged_in = logged[0]
    log_status = logged[1]


def logout():
    with open("logged.json", "w") as file1:
        json.dump([False, "Login"], file1)
    change_log_status()
    # return redirect(url_for("index"))


def valid_signup(users, username):
    for user in users:
        if user["username"] == username:
            return False
    return True


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if "log_in_out" in request.form:
            if request.form["log_in_out"] == "Login":
                return redirect(url_for("login"))
            else:
                logout()
                return redirect(url_for("index"))
        # elif "log_in_out2" in request.form:
        #     if request.form["log_in_out2"] == "Login":
        #         return redirect(url_for("login"))
        #     else:
        #         logout()
        #         return redirect(url_for("index"))


    # with open("logged.json", "r") as file1:
    return render_template("hello.html", log_msg=log_status)


@app.route("/login", methods=["POST", "GET"])
def login():
    # log_msg = "Enter the Following"
    if logged_in:
        return redirect(url_for("home"))
    if request.method == "POST":
        user = request.form["name"]
        pw = request.form["pw"]
        with open("user_data.json", "r") as file1:
            users = json.load(file1)
        if check_login(users, user, pw):
            with open("logged.json", "w") as file2:
                json.dump([True, "Log Out"], file2)
            change_log_status()
            return redirect(url_for("home"))
        else:
            msg = "Invalid Username or Password."
            return render_template("login.html", message=msg, log_msg=log_status, status="disabled")
    else:
        return render_template("login.html", log_msg=log_status, status="disabled")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if logged_in:
        return redirect(url_for("home"))
    if request.method == "POST":
        user = request.form["name"]
        pw = request.form["pw"]
        # return render_template("signup.html", message=[user, pw], log_msg="Set Up Credentials", status="disabled")
        if user == "" or pw == "":
            msg = "Both fields are required! Please don't leave any field empty."
            return render_template("signup.html", message=msg, log_msg=log_status, status="disabled")
        new_user = {"username": user, "password": pw}
        with open("user_data.json", "r") as file1:
            users = json.load(file1)
            if not valid_signup(users, user):
                msg = "User with this username already exists. Please choose another username"
                return render_template("signup.html", message=msg, log_msg=log_status, status="disabled")
        users.append(new_user)
        with open("user_data.json", "w") as file2:
            json.dump(users, file2)
        with open("logged.json", "w") as file3:
            json.dump([True, "Log Out"], file3)
        change_log_status()
        return redirect("home")
    else:
        return render_template("signup.html", log_msg=log_status, status="disabled")


@app.route("/about", methods=["POST", "GET"])
def about():
    if request.method == "POST":
        if "log_in_out" in request.form:
            if request.form["log_in_out"] == "Login":
                return redirect(url_for("login"))
            else:
                logout()
                return redirect(url_for("index"))
    else:
        return render_template("about.html", log_msg=log_status)


@app.route("/home", methods=["POST", "GET"])
def home():
    """Home Page"""
    if not logged_in:
        return redirect("login")
    elif request.method == "POST":
        # return render_template("home.html", msg=request.form, log_msg=log_status)
        with open('data.json', 'r') as file:
            data = json.load(file)

        if "log_in_out" in request.form:
            if request.form["log_in_out"] == "Login":
                return redirect(url_for("login"))
            else:
                logout()
                return redirect(url_for("index"))

        elif "sub" in request.form:
            srch = request.form.get('search')
            if evaluate_movies(srch):
                return render_template("home.html", log_msg=log_status, data=dataa, ms="")
            else:
                dataa.clear()
                return render_template("home.html", log_msg=log_status, data=dataa, ms="You have not added this movie")
        elif "addd" in request.form:
            return redirect(url_for("add"))

        elif "rem" in request.form:
            return redirect(url_for("remove"))


    else:
        name = []
        author = []
        status = []
        ms2 = ""
        with open("data.json") as file1:
            data = json.load(file1)

        return render_template("home.html", log_msg=log_status, data=data, msg=ms2)


@app.route("/remove", methods=["POST", "GET"])
def remove():
    if request.method == "POST":
        name = request.form['name']
        for i, j in enumerate(data):
            if j["name"] == name:
                break
        del data[i]
        with open("data.json", "w") as write1:
            json.dump(data, write1)
        return redirect(url_for("home"))

    else:
        return render_template('del.html')


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        lang = request.form.get("lang")
        status = request.form.get("status")

        with open("data.json", "w") as file:
            data.append({"name": name, "lang": lang, "status": status, "month": month})
            json.dump(data, file)

        return redirect('/home')

    else:
        return render_template('admin.html')


def evaluate_movies(movie):
    for i in data:
        if movie == i["name"]:
            if dataa != []:
                with open('dataa.json', 'w') as file:
                    dataa.clear()
                    dataa.append(i)
                    json.dump(dataa, file)
            else:
                dataa.append(i)
                with open('dataa.json', 'w') as file:
                    json.dump(dataa, file)
            return True

        else:
            lom = []
            for i in data:
                lom.append(i['name'])
            if movie not in lom:
                return False


if __name__ == "__main__":
    logged_in, log_status = startup()
    app.run(debug=True, host= "192.168.0.101")
