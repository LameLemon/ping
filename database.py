import sqlite3


class Database():
    def __init__(self, db_location):
        self.__DB_LOCATION = db_location
        self.__connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor = self.__connection.cursor()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY,
                name VARCHAR(50) UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS service (
                id INTEGER PRIMARY KEY,
                name VARCHAR(50),
                url VARCHAR(2084),
                status_code INTEGER,
                category_id REFERENCES category(id)
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

    def insert_category(self, name):
        sql = """
            INSERT INTO category (name)
            VALUES (?)
        """
        try:
            self.cursor.execute(sql, (name, ))
            self.__connection.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def check_category_by_name(self, name):
        sql = """
            SELECT *
            FROM category
            WHERE name = ?
            COLLATE NOCASE
        """
        self.cursor.execute(sql, (name, ))
        return self.cursor.fetchone()


    def insert_service(self, name, url, status_code, category_name):
        category = self.check_category_by_name(category_name)
        if not category:
            return False
        category = category[0]

        sql = """
            INSERT INTO service (name, url, status_code, category_id)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(sql, (name, url, status_code, category))
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
            SELECT service.name, service.url, max(checks.timestamp), checks.status, category.name
            FROM service
            INNER JOIN checks ON service.id = checks.service_id
            INNER JOIN category ON category.id = service.category_id
            GROUP BY service.id
        """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()

    def __del__(self):
        self.__connection.close()
