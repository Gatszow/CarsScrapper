import mysql.connector
from secret import password
from scrapper import CarsScrapper


def difference(list1, list2):
    list_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return list_dif


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
            'Mileage_km MEDIUMINT UNSIGNED, '
            'ProductionYear YEAR, '
            'FuelType ENUM("Benzyna", "Benzyna+LPG", "Benzyna+CNG", '
            '"Diesel", "Elektryczny", "Etanol", "Hybryda", "Wodór", "Failed to get"), '
            'EngineSize_cm3 SMALLINT UNSIGNED, '
            'URL VARCHAR(500), '
            'Price MEDIUMINT UNSIGNED, '
            'Currency VARCHAR(10), '
            'Negotiable ENUM("True", "False", "Failed to get") NOT NULL)'
        )
        self.values = CarsScrapper.search
        self.without = []

    def check(self):
        self.values = list(set(self.values))
        self.mycursor.execute('SELECT * FROM Cars')
        for record in self.mycursor:
            for row in range(len(self.values)):
                if record[1] == self.values[row][0] and record[2] == self.values[row][1] \
                        and record[3] == self.values[row][2] and record[8] == self.values[row][7] \
                        and record[9] == self.values[row][8]:

                    self.without.append(self.values[row])

        values = difference(self.without, self.values)

        return values

    def add(self):
        data = self.check()
        self.mycursor.executemany('INSERT INTO Cars Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                  data)
        self.mydb.commit()

    def show(self):
        self.mycursor.execute('SELECT * FROM Cars')
        for x in self.mycursor:
            print(x)


DatabaseUpdater().show()
