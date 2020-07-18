import mysql.connector
from secret import password
from scrapper import CarsScrapper


class DatabaseUpdater(object):
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password,
            database='test'
        )

        self.mycursor = self.mydb.cursor()

        # Database creation
        # mycursor.execute('CREATE DATABASE test')

        # Table creation
        self.mycursor.execute(
            'CREATE TABLE IF NOT EXISTS Cars ('
            'CarID INT PRIMARY KEY AUTO_INCREMENT, '
            'Make VARCHAR(30), '
            'Model VARCHAR(30), '
            'Mileage MEDIUMINT UNSIGNED, '
            'ProductionYear YEAR, '
            'FuelType ENUM("Benzyna", "Benzyna+LPG", "Benzyna+CNG", '
            '"Diesel", "Elektryczny", "Etanol", "Hybryda", "Wodór"), '
            'EngineSize SMALLINT UNSIGNED, '
            'URL VARCHAR(500), '
            'Price MEDIUMINT UNSIGNED, '
            'Currency VARCHAR(10), '
            'Negotiable ENUM("True", "False", "Failed to get") NOT NULL)'
        )

    def add(self):
        self.mycursor.executemany('INSERT INTO Cars Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                                  % CarsScrapper.search)
        self.mydb.commit()

    def update(self):
        pass
