from datetime import datetime
from database import Database
import requests

def check_loop():
    db = Database("./ping.db")
    services = db.get_all_services()
    for service in services:
        status = http_check(service[2], service[3])
        db.insert_check(datetime.timestamp(datetime.now()), status, service[0])
        print(service[1], status)

def http_check(url, status_code):
    r = requests.get(url)
    if r.status_code == status_code:
        return True
    print(r.status_code)
    return False

