import sqlite3


class Database():
    def __init__(self, db_location):
        self.__DB_LOCATION = db_location
        self.__connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor = self.__connection.cursor()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS service (
                id INTEGER PRIMARY KEY,
                name VARCHAR(50),
                url VARCHAR(2084),
                status_code INTEGER
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS checks (
                id INTEGER PRIMARY KEY,
                timestamp INTEGER,
                status INTEGER,
                service_id REFERENCES service(id)
            )
        """)


    def insert_service(self, name, url, status_code):
        sql = """
            INSERT INTO service (name, url, status_code)
            VALUES (?, ?, ?)
        """
        self.cursor.execute(sql, (name, url, status_code))
        self.__connection.commit()

    def check_service_by_name(self, name):
        sql = """
            SELECT *
            FROM service
            WHERE name = ?
            COLLATE NOCASE
        """
        self.cursor.execute(sql, (name, ))
        return self.cursor.fetchall()

    def get_all_services(self):
        sql = """
            SELECT *
            FROM service
        """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()


    def insert_check(self, timestamp, status, service_id):
        sql = """
            INSERT INTO checks (timestamp, status, service_id)
            VALUES (?, ?, ?)
        """
        self.cursor.execute(sql, (timestamp, status, service_id))
        self.__connection.commit()
        return True

    def get_service_check(self):
        sql = """
            SELECT service.name, service.url, max(checks.timestamp), checks.status
            FROM service
            INNER JOIN checks ON service.id = checks.service_id
            GROUP BY service.id
        """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()

    def __del__(self):
        self.__connection.close()
