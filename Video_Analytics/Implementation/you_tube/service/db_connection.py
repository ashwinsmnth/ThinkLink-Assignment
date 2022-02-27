
import os
import sys
import sqlite3
from sqlite3 import Error

from Video_Analytics.Implementation.you_tube.db.db_tables import SQL_CREATE_VIDEO_ANALYTICS_TABLE, SQL_INDEX_CREATION, \
    VIDEO_ANALYTICS_DATABASE_TABLE, VIDEO_ANALYTICS_DB_COLUMNS


class DBConnection(object):

    def __init__(self, db_file=None):
        self._db_file = db_file or os.path.join(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "db"), "you_tube_analytics.db")
        self._db_connection = self.create_connection()
        self._initialize()

    def _initialize(self):
        self.execute_statement(SQL_CREATE_VIDEO_ANALYTICS_TABLE)
        self.execute_statement(SQL_INDEX_CREATION)
        print("DB tables are created.")

    def create_connection(self):
        """
        Creates a database connection to a SQLite database
        """
        try:
            conn = sqlite3.connect(self._db_file)
            print("SQLite3 connection established")
            return conn
        except Error as e:
            print("SQLite3 connection failed with error: {}".format(str(e)))
            sys.exit(-1)

    def close_connection(self):
        """
        Closes database connection
        """
        self._db_connection.close()

    def execute_statement(self, sql_statement, expecting_return=False):
        """
        Executes given SQL statements
        :param sql_statement: SQL statement
        :type sql_statement: str
        :param expecting_return: If enabled, then result will be sent back else not
        :type expecting_return: bool
        :return:
        """
        try:
            cursor = self._db_connection.cursor()
            response = cursor.execute(sql_statement)
            if expecting_return:
                return response.fetchall()
        except Error as e:
            print("Exception occurred while executing db statement: {}".format(str(e)))
            sys.exit(-1)

    def insert_data(self, data, db_table=VIDEO_ANALYTICS_DATABASE_TABLE, db_columns=VIDEO_ANALYTICS_DB_COLUMNS):
        """
        Inserts data into db table specified
        :param data: Data to be inserted
        :param db_table: DB table name
        :param db_columns: DB Columns
        :return:
        """
        sql = '''INSERT INTO {}({})VALUES({}) '''.format(db_table, db_columns, "?,"*4+"?")
        cur = self._db_connection.cursor()
        cur.executemany(sql, data)
        self._db_connection.commit()
