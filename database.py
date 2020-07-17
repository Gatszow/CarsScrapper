import mysql.connector
from secret import password
from scrapper import CarsScrapper


class DatabaseUpdater():
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
        '''        mycursor.execute(
            'CREATE TABLE Cars ('
            'CarID INT PRIMARY KEY AUTO_INCREMENT, '
            'Make VARCHAR(30), '
            'Model VARCHAR(30), '
            'Mileage MEDIUMINT UNSIGNED, '
            'ProductionYear YEAR, '
            'FuelType ENUM("Benzyna", "Benzyna+LPG", "Benzyna+CNG", "Diesel", "Elektryczny", "Etanol", "Hybryda", "Wodór"), '
            'EngineSize SMALLINT UNSIGNED, '
            'URL VARCHAR(500), '
            'Price MEDIUMINT UNSIGNED,'
            'Currency VARCHAR(10))'
        )
        '''

    def ADD(self):
        self.mycursor.executemany('INSERT INTO Cars Values (%s, %s, %s, %s, %s, %s, %s, %s, %s)' % CarsScrapper.search())
        self.mydb.commit()