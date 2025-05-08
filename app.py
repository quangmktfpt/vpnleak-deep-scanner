from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def get_ip_info(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json")
        return r.json()
    except:
        return {}

@app.route("/")
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_info = get_ip_info(ip)
    return render_template("index.html", ip=ip, ip_info=ip_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
