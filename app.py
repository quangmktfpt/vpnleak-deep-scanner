from flask import Flask, request, render_template
import requests
import geoip2.database

app = Flask(__name__)

# Đường dẫn đến file MaxMind GeoLite2 City
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

ABUSEIPDB_API_KEY = "demo"  # Thay bằng key thật nếu muốn kiểm tra blacklist

def get_ip_info(ip):
    ipinfo = {}
    try:
        city = reader.city(ip)
        ipinfo["city"] = city.city.name
        ipinfo["country"] = city.country.name
        ipinfo["timezone"] = city.location.time_zone
    except:
        ipinfo["city"] = None
        ipinfo["country"] = None
        ipinfo["timezone"] = None

    try:
        abuse_data = requests.get(
            f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90",
            headers={"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"}
        ).json()
        ipinfo["abuseScore"] = abuse_data.get("data", {}).get("abuseConfidenceScore", -1)
        ipinfo["hostType"] = abuse_data.get("data", {}).get("usageType", "Unknown")
    except:
        ipinfo["abuseScore"] = -1
        ipinfo["hostType"] = "Unknown"
    return ipinfo

@app.route("/")
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_info = get_ip_info(ip)
    return render_template("index.html", ip=ip, ip_info=ip_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
