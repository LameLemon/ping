from datetime import datetime
from database import Database
import requests
import argparse
import json


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


def update_config():
    with open('config.json') as json_file:
        data = json.load(json_file)

    db = Database("./ping.db")
    db.create_tables()

    for category in data.get("categories", []):
        cat_name = category.get("name")
        if not db.check_category_by_name(cat_name):
            db.insert_category(cat_name)

        for service in category.get("services", []):
            name = service.get("name")
            if not db.check_service_by_name(name):
                db.insert_service(
                    name, service.get("url"),
                    service.get("status_code"), cat_name
                )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--check",
        help="check all services", action="store_true"
    )
    parser.add_argument(
        "-u", "--update_config",
        help="update database with new config", action="store_true"
    )

    args = parser.parse_args()
    if args.check:
        check_loop()

    if args.update_config:
        update_config()


if __name__ == "__main__":
    main()
