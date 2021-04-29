import os
from flask import Flask, redirect, url_for, render_template, request
from getmac import get_mac_address as gma
from pathlib import Path
import json

# print(gma())



# path = Path(__file__).parent.absolute()
# print(path)
# exit()
# os.chdir(Path(__file__).parent.absolute())
# test_pycharm_presence = "pycharm" not in str(Path(__file__).cwd()).lower()
# test_path = Path(__file__).cwd() == Path(__file__).parent.absolute()
# if this file is being run inside pycharm, then, well, don't run it
# assert test_pycharm_presence, "Don't Run this file in PyCharm. You know why!"
# assert test_path, """Make sure you are running this file from the folder which holds it. E.g., if the path of this file is D:\\movie_archive\\app.py, then make sure you are in
# in the movie_archive folder before running this file (from the terminal or the command prompt)"""
# path = Path(__file__).parent.absolute()
# print(path)
# exit()

app = Flask(__name__)
# json_path = os.path.join(Path(__file__).parent.absolute(), "json")
json_path = os.path.join(Path(__file__).parent, "json")
req_vals = {}
print(req_vals)
def startup():
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    filepath1 = os.path.join(json_path, "user_data.json")
    if not os.path.exists(filepath1):
        with open(filepath1, "w") as write1:
            json.dump([], write1)
    filepath2 = os.path.join(json_path, "logged.json")
    if not os.path.exists(filepath2):
        with open(filepath2, "w") as write2:
            json.dump({}, write2)
    filepath3 = os.path.join(json_path, "data.json")
    if not os.path.exists(filepath3):
        with open(filepath3, "w") as write3:
            json.dump({}, write3)
    with open(filepath2, "r") as read1:
        logged = json.load(read1)
    users = []
    logged_in_list = []
    log_stats = []
    mac_list = list(logged.keys())
    for i in mac_list:
        logged_in_list.append(logged[i][0])
        log_stats.append(logged[i][1])
        users.append(logged[i][2])
    # filepath4 = os.path.join(Path(__file__).parent)
    files = [filepath1, filepath2, filepath3]
    keys = ["user_data.json", "logged.json", "data.json"]
    filepath = dict(zip(keys, files))
    add_notif((logged_in_list, log_stats, mac_list, users, filepath))
    return logged_in_list, log_stats, mac_list, users, filepath


def check_login(username: str, password: str) -> bool:
    with open(req_vals["filepath"]["user_data.json"], "r") as file:
        data = json.load(file)
    add_notif(data)
    # file = open("notifs.txt", "a")
    # file.write(str(data))
    # file.close()
    for i in data:
        if i["username"] == username and i["pw"] == password:
            return True
    return False

def delete_movie(user, name):
    with open("data.json", "r") as file:
        data = json.load(file)
    for i,j in data.enumerate():
        if i  == user:
            for k in j:
                if k["name"] == name:
                    del data[k]


def change_log_status(addr, data):
    # with open("json/logged.json", "r") as file1:
    #     data = json.load(file1)
    if addr not in req_vals["mac_list"]:
        req_vals["mac_list"].append(addr)
        to_append = ("logged_in_list", "log_status", "users")
        for i in range(len(data[addr])):
            req_vals[to_append[i]].append(data[addr][i])
        # req_vals["logged_in_list"].append(addr)
        # req_vals["log_status"].append(addr)
    # i = req_vals["mac_list"].index(addr)
    else:
        i = req_vals["mac_list"].index(addr)
        req_vals["logged_in_list"][i], req_vals["log_status"][i], req_vals["users"][i] = tuple(data[addr])
    # if username is not None:
    #     with open("notifs.json", "a") as append1:
    #         json.dump("adding username to req_vals dictionary!", append1)
    #     req_vals["username"] = username


def logout(addr):
    with open(req_vals["filepath"]["logged.json"], "r") as file1:
        data = json.load(file1)
    data[addr] = [False, "Login", None]
    with open(req_vals["filepath"]["logged.json"], "w") as file2:
        json.dump(data, file2)
    change_log_status(addr, data)
    # return redirect(url_for("index"))


def log_in(addr, user):
    # user = req_vals["users"][req_vals["mac_list"].index(addr)]
    # add_notif(req_vals["filepath"]["logged.json"])
    # using r+ in the line below ensures that the data of the file
    # does not get erased on opening the file, whereas the w+ mode
    # erases the data of the file making reading data unsuccessful
    logged_json = req_vals["filepath"]["logged.json"]
    with open(logged_json, "r") as file1:
        # add_notif(os.path.realpath(file1.name))
        # add_notif(os.getcwd())
        data = json.load(file1)
    with open(logged_json, "w") as file2:
        data[addr] = [True, "Logout", user]
        json.dump(data, file2)
        change_log_status(addr, data)


def valid_signup(users, username):
    for user in users:
        if user["username"] == username:
            return False
    return True


def add_notif(msg):
    """adds msg to the notifs.txt file as a string"""
    with open("notifs.txt", "a") as file1:
        file1.write(str(msg)+"\n")   


def get_status(addr):
    # addr_present = addr in req_vals["mac_list"]
    add_notif(req_vals["mac_list"])
    add_notif(addr in req_vals["mac_list"])
    if addr in req_vals["mac_list"]:
        index = req_vals["mac_list"].index(addr)
        return req_vals["log_status"][index]
    return "Login"


def get_log(addr):
    """Returns True if user is logged in, else False"""
    if addr in req_vals["mac_list"]:
        index = req_vals["mac_list"].index(addr)
        return req_vals["logged_in_list"][index]
    return False


def add_user(username, pw):
    with open(req_vals["filepath"]["user_data.json"], "+") as file:
        users = json.load(file)
        users.append({"username": username, "pw": pw})
        json.dump(users, file)


def open_file(name: str, mode="r", return_value=False, write_val=None, write_key=None, write_data=None):
    with open(req_vals["filepath"][name], mode) as file:
        if mode == "r":
            return json.load(file)
        elif mode == "w":
            write_data[write_key] = write_val
            json.dump(write_data, file)
        elif mode == "a":
            file.write(str(write_data)+"\n")


@app.route("/", methods=["POST", "GET"])
def index():
    user_address = request.remote_addr
    add_notif(user_address)
    # return "<h1>HEY! ISHAN! LAST TIME, YOU HAD LEFT STUFF TOTALLY" \
    # "UNFINISHED. SO... you know what to do. do it!</h1>"
    if request.method == "POST":
        if "log_in_out" in request.form:
            if request.form["log_in_out"] == "Login":
                return redirect(url_for("login"))
            else:
                logout(user_address)
                return render_template("hello.html", log_msg=get_status(user_address))
    # with open("logged.json", "r") as file1:
    return render_template("hello.html", log_msg=get_status(user_address))


@app.route("/login/", methods=["POST", "GET"])
def login():
    user_address = request.remote_addr
    # log_msg = "Enter the Following
    if request.method == "POST":
        user, pw = request.form["name"], request.form["pw"]
        if check_login(user, pw):
            log_in(user_address, user)
            return redirect(url_for("home"))
        else:
            msg = "Invalid Username or Password"
            # msg = "Invalid Username or Password. %s %s" % (user, pw)
            return render_template("login.html", message=msg, log_msg=get_status(user_address), status="disabled")
    else:
        if get_log(user_address):
            return redirect(url_for("home"))
        return render_template("login.html", log_msg=get_status(user_address), status="disabled")


@app.route("/signup/", methods=["POST", "GET"])
def signup():
    user_address = request.remote_addr
    if request.method == "POST":
        user, pw = request.form["name"], request.form["pw"]
        # return render_template("signup.html", message=[user, pw], log_msg="Set Up Credentials", status="disabled")
        if "" in [user, pw]:
            msg = "Both fields are required! Please don't leave any field empty."
            return render_template("signup.html", message=msg, log_msg=get_status(user_address), status="disabled")
        new_user = {"username": user, "pw": pw}
        with open("json/user_data.json", "r") as file1:
            users = json.load(file1)
        if not valid_signup(users, user):
            msg = "User with this username already exists. Please choose another username"
            return render_template("signup.html", message=msg, log_msg=get_status(user_address), status="disabled")
        users.append(new_user)
        with open("json/user_data.json", "w") as file2:
            json.dump(users, file2)
        with open(req_vals["filepath"]["data.json"], "r") as file3:
            data = json.load(file3)
        data[user] = []
        with open(req_vals["filepath"]["data.json"], "w") as file4:
            json.dump(data, file4)
        log_in(user_address, user)
        # change_log_status(user)
        return redirect(url_for("home"))
    else:
        if get_log(user_address):
            return redirect(url_for("home"))
        return render_template("signup.html", log_msg=get_status(user_address), status="disabled")


@app.route("/add", methods = ["POST", "GET"])
def add():
    msg = ""
    with open("json/data.json", "r") as file:
        data = json.load(file)
    addr = request.remote_addr
    if request.method == "POST":
        list_ = req_vals["mac_list"]
        index = list_.index(addr)
        user = req_vals["users"][index]
        user_data = data[user]
        name = request.form.get("name")
        lang = request.form.get("lang")
        month = request.form.get("month")
        status = request.form.get("status")
        list_of_names = []
        for i in user_data:
            list_of_names.append(i["name"])
        if name not in list_of_names:
            with open("json/data.json", "w") as file2:
                user_data.append({"name": name, "lang": lang, "month": month, "status":status})
                json.dump(data, file2)
        else:
            msg = "Movie already added"
        return redirect("/home")
    else:
        return render_template("add.html", msg = msg)

            
@app.route("/about/", methods=["POST", "GET"])
def about():
    user_address = request.remote_addr
    if request.method == "POST":
        if "log_in_out" in request.form:
            if request.form["log_in_out"] == "Login":
                return redirect(url_for("login"))
            else:
                logout(user_address)
                return render_template("about.html", log_msg=get_status(user_address))
    else:
        return render_template("about.html", log_msg=get_status(user_address))


@app.route("/remove", methods=["POST", "GET"])
def remove():
    msg = ""
    if request.method == "POST":
        name = request.form['name']
        with open("json/data.json", "r") as file:
            data = json.load(file)

        addr = request.remote_addr
   
        list_ = req_vals["mac_list"]
        index = list_.index(addr)
        user = req_vals["users"][index]
        user_data = data[user]
        for i in user_data:
            if i["name"] == name:
                index = user_data.index(i)
                del user_data[index]
                break
            else:
                msg = "no such movie exists"
        with open("json/data.json", "w") as file1:
            json.dump(data, file1)
        return redirect("/home")

    else:
        return render_template('del.html', msg = msg)

@app.route("/home/", methods=["POST", "GET"])
def home():
    """Home Page"""
    user_address = request.remote_addr
    if request.method == "POST":
        result = tuple(request.form.keys())
        with open("notifs.txt", "a") as append1:
            append1.write(str(result)+"\n")
        # return render_template("home.html", msg=request.form, log_msg=log_status)
        if "log_in_out" in request.form:
            logout(user_address)
            return redirect(url_for("index"))
        elif "del_value" in request.form:
            return redirect("/remove")
        else:
            return redirect("/add")
    else:
        if not get_log(user_address):
            return redirect(url_for("login"))
        with open("json/data.json") as file1:
            # return req_vals
            data = json.load(file1)[req_vals["users"][req_vals["mac_list"].index(user_address)]]
            add_notif(data)
        return render_template("home.html", log_msg=get_status(user_address) , data=data)


@app.route("/confirm_user/", methods=["POST", "GET"])
def confirm_user():
    """Asks use for password after on re-enter to website's only-authorised-people
     stuff if they hadn't logged out, for safety"""
    if request.method == "POST":
        pass
    else:
        return render_template("confirm_user.html", log_msg="Fix this Ishan")



@app.route("/<blah>/")
def any_else(blah):
    return "%s %s" % (blah, request.remote_addr)


if __name__ == "__main__":
    req_vals["logged_in_list"], req_vals["log_status"], req_vals["mac_list"], \
    req_vals["users"], req_vals["filepath"] = startup()
    app.run(debug=True, host = '192.168.0.101')

