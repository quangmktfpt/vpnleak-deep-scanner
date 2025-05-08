from flask import Flask, request, render_template
import requests

app = Flask(__name__)

ABUSEIPDB_API_KEY = "demo"  # Thay bằng API key thật nếu cần kiểm tra nghiêm túc

def get_ip_info(ip):
    try:
        ipinfo = requests.get(f"https://ipinfo.io/{ip}/json").json()
        abuse_data = requests.get(
            f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90",
            headers={"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"}
        ).json()
        ipinfo["abuseScore"] = abuse_data.get("data", {}).get("abuseConfidenceScore", -1)
        ipinfo["hostType"] = abuse_data.get("data", {}).get("usageType", "Unknown")
        return ipinfo
    except:
        return {}

@app.route("/")
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_info = get_ip_info(ip)
    return render_template("index.html", ip=ip, ip_info=ip_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
