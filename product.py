from exceptions import TooSmallNumberOfRowError
from scrapper import CarsScrapper
from random import random
from time import sleep


class ProductUpdater(object):
    def __init__(self):
        pass

    def update(self):
        pass
        # makes, models, mileages, years, fuels, engine_sizes, urls, prices, currencies = CarsScrapper().search()

    '''def delete(self, start_row: int, end_row: int):
        pass
        try:
            if start_row > 1 and end_row > 1:
                self.sheet.delete_dimension('ROWS', start_row, end_row)

            else:
                raise TooSmallNumberOfRowError

        except TooSmallNumberOfRowError:
            print('Row number must be number 2 or bigger')'''

    '''def show(self):
        pass
        self.sheet.get_all_records()'''
