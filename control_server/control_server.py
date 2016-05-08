from flask import Flask, request, render_template, url_for
import cec_power
from pytomation.interfaces import cm11a, Serial
import re
import requests
import subprocess
import remote_command

app = Flask(__name__)

app.secret_key = "NoneYaBusiness"

app = Flask(__name__)

x10 = cm11a.CM11a(Serial("/dev/x10serial", 4800))

x10_url_dict = {"A1": "http://remote.local:5500",
                "A2": "http://bedroom.local:5500",
                "A3": "http://piden.local:5500"
                }

def x10_response(url):
    response = requests.get(url)
    if response.text == "1":
        return "1"
    elif response.text == "0":
        return "0"
    else:
        return "error"

@app.route("/",methods=["GET","POST"])
def ps4_index():
    if request.method == "POST":
        print("hello")
        cec_power.lib.Transmit(cec_power.lib.CommandFromString("14:44:" + cec_power.ps4_dict["up"]))
        return render_template("index.html")
    else:
        return render_template("index.html")

@app.route("/ps4_command/<cmd>", methods=["GET","POST"])
def foo(cmd):
    cec_power.lib.Transmit(cec_power.lib.CommandFromString("14:44:" + cec_power.ps4_dict[cmd]))
    return "ok"

@app.route("/cec/<device>/<cmd>")
def ps4_command(device,cmd):
    if cmd == "on":
        cec_power.power_on_device(int(device))
        return "ok"
    elif cmd == "off":
        if device == "4":
            subprocess.Popen("ps4-waker -t 5000 standby", shell=True)
        cec_power.standby_device(int(device))
        return "ok"
    elif cmd == "status":
        return str(cec_power.power_status(int(device)))

@app.route("/x10/<device>/<command>")
def x10_command(device, command):
    if command == "on":
        x10.on(device)
    elif command == "off":
        x10.off(device)
    elif command == "status":
        return x10_response(x10_url_dict[device])
    return "ok"

@app.route("/receiver/<command>")
def receiver_command(command):
    remote_command.remote_com(command)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
