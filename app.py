from flask import Flask, render_template
from datetime import datetime
from database import Database

app = Flask(__name__)

@app.route("/")
def home():
    db = Database("./ping.db")
    services = db.get_service_check()
    services_date = []
    for service in services:
        services_date.append([
            service[0],
            datetime.fromtimestamp(service[2]).strftime("%d/%m/%y %H:%M:%S"),
            service[3]
        ])
    return render_template("index.html", services=services_date)

if __name__ == '__main__':
    db = Database("./ping.db")
    db.create_tables()
    app.run()