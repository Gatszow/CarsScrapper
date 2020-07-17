from selenium import webdriver
from exceptions import WrongThingToGetError


def convert_to_str(input_seq):
    string = ' '.join(input_seq)
    return string


def get_price_and_currency(price_with_currency):
    price_with_currency = price_with_currency.replace(' ', '')
    name_of_currency = []
    for z in range(len(price_with_currency)):
        try:
            int(price_with_currency)
            break
        except ValueError:
            name_of_currency.append(price_with_currency[len(price_with_currency) - 1:])
            price_with_currency = price_with_currency[:-1]
    name_of_currency.reverse()
    name_of_currency = ''.join(name_of_currency)
    return price_with_currency, name_of_currency


class CarsScrapper(object):
    def __init__(self):
        '''self.url = 'https://www.otomoto.pl/osobowe/' \
                   '?search%5Bfilter_float_price%3Ato%5D=20000&search' \
                   '%5Bfilter_float_mileage%3Ato%5D=150000&search' \
                   '%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol&search' \
                   '%5Bfilter_enum_fuel_type%5D%5B1%5D=petrol-lpg&search' \
                   '%5Bfilter_enum_damaged%5D=0&search' \
                   '%5Bfilter_enum_no_accident%5D=1&search' \
                   '%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D' \
                   '%5B0%5D=&search%5Bcountry%5D=&view=list'
                   '''
        self.url = 'https://www.otomoto.pl/osobowe/alfa-romeo/?search%5Bfilter_float_price%3Ato%5D=20000&search%5Bfilter_float_mileage%3Ato%5D=150000&search%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol&search%5Bfilter_enum_fuel_type%5D%5B1%5D=petrol-lpg&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_no_accident%5D=1&search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=&view=list'

        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        self.list_of_tuples = []

        self.makes = []
        self.excluded_makes = ['Alfa Romeo', 'Aston Martin', 'De Lorean', 'Land Rover', 'DS Automobiles']

        self.models = []
        self.mileages = []
        self.years = []
        self.fuels = []
        self.engine_sizes = []
        self.urls = []
        self.prices = []
        self.currencies = []

    def get_products_make_and_model(self, title_class_name: str):
        titles = self.driver.find_elements_by_class_name(title_class_name)
        for title in titles:
            print(title.text)
            if title.text in self.excluded_makes:
                self.models.append(convert_to_str(title.text.split()[2:]))
                self.makes.append(title.text.split()[:2])
            else:
                self.models.append(convert_to_str(title.text.split()[1:]))
                self.makes.append(title.text.split()[0])

        len_of_elements = len(self.models)

        return self.makes, self.models, len_of_elements

    def get_products(self, thing_to_get, counter):
        try:
            if thing_to_get == 'mileage':
                for i in range(1, counter+1):
                    mileage = self.driver.find_element_by_xpath(
                        f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}'
                        f']/div[2]/ul/li[2]/span')
                    self.mileages.append(mileage.text)

                return self.mileages

            elif thing_to_get == 'year':
                for i in range(1, counter + 1):
                    year = self.driver.find_element_by_xpath(
                        f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}'
                        f']/div[2]/ul/li[1]/span')
                    self.years.append(year.text)

                return self.years

            elif thing_to_get == 'fuel':
                for i in range(1, counter + 1):
                    fuel = self.driver.find_element_by_xpath(
                        f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}'
                        f']/div[2]/ul/li[4]/span')
                    self.fuels.append(fuel.text)

                return self.fuels

            elif thing_to_get == 'engine_size':
                for i in range(1, counter + 1):
                    engine_size = self.driver.find_element_by_xpath(
                        f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}'
                        f']/div[2]/ul/li[3]/span')
                    self.engine_sizes.append(engine_size.text)

                return self.engine_sizes

            elif thing_to_get == 'url':
                a_class = self.driver.find_elements_by_class_name('offer-title__link')
                self.urls = [url.get_attribute('href') for url in a_class]

                return self.urls

            else:
                raise WrongThingToGetError

        except WrongThingToGetError:
            print('Wrong thing to get')

    def get_products_price_and_currency(self, counter):
        for i in range(1, counter + 1):
            price = self.driver.find_element_by_xpath(
                f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}'
                f']/div[2]/div[2]/div/div/span')
            value, currency = get_price_and_currency(price.text)
            self.prices.append(value)
            self.currencies.append(currency)
        return self.prices, self.currencies

    def search(self):
        makes, models, end_of_counter = self.get_products_make_and_model('offer-title__link')
        mileages = self.get_products('mileage', end_of_counter)
        years = self.get_products('year', end_of_counter)
        fuels = self.get_products('fuel', end_of_counter)
        engine_sizes = self.get_products('engine_size', end_of_counter)
        urls = self.get_products('url', end_of_counter)
        prices, currencies = self.get_products_price_and_currency(end_of_counter)

        for i in range(end_of_counter):
            temp = (makes[i], models[i], mileages[i], years[i], fuels[i],
                    engine_sizes[i], urls[i], prices[i], currencies[i])
            print(temp)
            self.list_of_tuples.append(temp)
            del temp

        return self.list_of_tuples


trying = CarsScrapper()
trying.search()
'''Poprawić get_products_make_and_model'''