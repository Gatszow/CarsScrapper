import gspread
from oauth2client.service_account import ServiceAccountCredentials
from exceptions import TooSmallNumberOfRowError
from scrapper import CarsScrapper
from gspread.exceptions import APIError
from random import random
from time import sleep


class ProductUpdater(object):
    def __init__(self, spreadsheet_name):
        self.make_column = 1
        self.model_column = 2
        self.mileage_column = 3
        self.year_column = 4
        self.fuel_column = 5
        self.engine_size_column = 6
        self.url_column = 7
        self.price_column = 8

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(spreadsheet_name).sheet1

    def update(self):
        makes, models, mileages, years, fuels, engine_sizes, urls, prices = CarsScrapper().search()
        for number in range(len(makes)):
            try:
                self.sheet.update_cell(number+2, self.make_column, makes[number])
                self.sheet.update_cell(number+2, self.model_column, models[number])
                self.sheet.update_cell(number+2, self.mileage_column, mileages[number])
                self.sheet.update_cell(number+2, self.year_column, years[number])
                self.sheet.update_cell(number+2, self.fuel_column, fuels[number])
                self.sheet.update_cell(number+2, self.engine_size_column, engine_sizes[number])
                self.sheet.update_cell(number+2, self.url_column, urls[number])
                self.sheet.update_cell(number+2, self.price_column, prices[number])

            except APIError:
                for i in range(2):
                    sleep(80 + random())

                    try:
                        self.delete(number+2, number+2)
                        self.sheet.update_cell(number+2, self.make_column, makes[number])
                        self.sheet.update_cell(number+2, self.model_column, models[number])
                        self.sheet.update_cell(number+2, self.mileage_column, mileages[number])
                        self.sheet.update_cell(number+2, self.year_column, years[number])
                        self.sheet.update_cell(number+2, self.fuel_column, fuels[number])
                        self.sheet.update_cell(number+2, self.engine_size_column, engine_sizes[number])
                        self.sheet.update_cell(number+2, self.url_column, urls[number])
                        self.sheet.update_cell(number+2, self.price_column, prices[number])
                        break

                    except APIError:
                        pass

    def delete(self, start_row: int, end_row: int):
        try:
            if start_row > 1 and end_row > 1:
                self.sheet.delete_dimension('ROWS', start_row, end_row)

            else:
                raise TooSmallNumberOfRowError

        except TooSmallNumberOfRowError:
            print('Row number must be number 2 or bigger')

    def show(self):
        self.sheet.get_all_records()
