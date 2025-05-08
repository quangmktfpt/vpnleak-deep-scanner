import os
import requests
import geoip2.database
from flask import Flask, request, render_template

app = Flask(__name__)

# Chuẩn hóa đường dẫn
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITY_DB = os.path.join(BASE_DIR, "GeoLite2-City.mmdb")
ASN_DB = os.path.join(BASE_DIR, "GeoLite2-ASN.mmdb")

city_reader = geoip2.database.Reader(CITY_DB)
asn_reader = geoip2.database.Reader(ASN_DB)

ABUSEIPDB_API_KEY = "demo"  # Thay bằng key thật nếu có

def get_ip_info(ip):
    ipinfo = {}

    # Lấy city/country
    try:
        city = city_reader.city(ip)
        ipinfo["city"] = city.city.name
        ipinfo["country"] = city.country.name
        ipinfo["timezone"] = city.location.time_zone
    except:
        ipinfo["city"] = None
        ipinfo["country"] = None
        ipinfo["timezone"] = None

    # Lấy ISP từ ASN
    try:
        asn = asn_reader.asn(ip)
        ipinfo["isp"] = asn.autonomous_system_organization
    except:
        ipinfo["isp"] = "Unknown"

    # Lấy loại IP từ AbuseIPDB
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
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ip_info = get_ip_info(ip)
    return render_template("index.html", ip=ip, ip_info=ip_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
