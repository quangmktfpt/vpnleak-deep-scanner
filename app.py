import requests
from flask import Flask, request, render_template

app = Flask(__name__)

IPREGISTRY_API_KEY = "tryout"  # Bạn nên tạo key riêng miễn phí ở ipregistry.co

def get_ip_info(ip):
    ipinfo = {
        "city": None,
        "country": None,
        "timezone": None,
        "isp": None,
        "hostType": None,
        "abuseScore": None
    }

    try:
        resp = requests.get(f"https://api.ipregistry.co/{ip}?key={IPREGISTRY_API_KEY}").json()
        ipinfo["city"] = resp.get("location", {}).get("city")
        ipinfo["country"] = resp.get("location", {}).get("country", {}).get("name")
        ipinfo["timezone"] = resp.get("time_zone", {}).get("id")
        ipinfo["isp"] = resp.get("connection", {}).get("organization")
        ipinfo["hostType"] = "Hosting" if resp.get("security", {}).get("is_hosting") else "Residential"
        ipinfo["abuseScore"] = "Blacklisted" if resp.get("security", {}).get("is_abuser") else "Clean"
    except Exception as e:
        print("Lỗi API:", e)

    return ipinfo

@app.route("/")
def index():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ip_info = get_ip_info(ip)
    return render_template("index.html", ip=ip, ip_info=ip_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
