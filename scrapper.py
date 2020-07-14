from selenium import webdriver
from exceptions import WrongThingToGetError


def convert_to_str(input_seq):
    string = ' '.join(input_seq)
    return string


class CarsScrapper(object):
    def __init__(self):
        self.url = 'https://www.otomoto.pl/osobowe/' \
                   '?search%5Bfilter_float_price%3Ato%5D=20000&search' \
                   '%5Bfilter_float_mileage%3Ato%5D=150000&search' \
                   '%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol&search' \
                   '%5Bfilter_enum_fuel_type%5D%5B1%5D=petrol-lpg&search' \
                   '%5Bfilter_enum_damaged%5D=0&search' \
                   '%5Bfilter_enum_no_accident%5D=1&search' \
                   '%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D' \
                   '%5B0%5D=&search%5Bcountry%5D=&view=list'

        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        self.makes = []
        self.models = []
        self.mileages = []
        self.years = []
        self.fuels = []
        self.engine_sizes = []
        self.urls = []
        self.prices = []

    def get_products_make_and_model(self, title_class_name: str):
        titles = self.driver.find_elements_by_class_name(title_class_name)

        self.models = [convert_to_str(title.text.split()[1:]) for title in titles]
        self.makes = [title.text.split()[0] for title in titles]
        len_of_elements = len(self.models)

        return self.makes, self.models, len_of_elements

    def get_products(self, thing_to_get, counter):
        try:
            if thing_to_get == 'mileage':
                for i in range(1, counter+1):
                    mileage = self.driver.find_element_by_xpath(f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}]/div[2]/ul/li[2]/span')
                    self.mileages.append(mileage.text)

                return self.mileages

            elif thing_to_get == 'year':
                for i in range(1, counter + 1):
                    year = self.driver.find_element_by_xpath(f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}]/div[2]/ul/li[1]/span')
                    self.years.append(year.text)

                return self.years

            elif thing_to_get == 'fuel':
                for i in range(1, counter + 1):
                    fuel = self.driver.find_element_by_xpath(f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}]/div[2]/ul/li[4]/span')
                    self.fuels.append(fuel.text)

                return self.fuels

            elif thing_to_get == 'engine_size':
                for i in range(1, counter + 1):
                    engine_size = self.driver.find_element_by_xpath(f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}]/div[2]/ul/li[3]/span')
                    self.engine_sizes.append(engine_size.text)

                return self.engine_sizes

            elif thing_to_get == 'url':
                a_class = self.driver.find_elements_by_class_name('offer-title__link')
                self.urls = [url.get_attribute('href') for url in a_class]

                return self.urls

            elif thing_to_get == 'price':
                for i in range(1, counter + 1):
                    price = self.driver.find_element_by_xpath(f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}]/div[2]/div[2]/div/div/span')
                    self.prices.append(price.text)

                return self.prices

            else:
                raise WrongThingToGetError

        except WrongThingToGetError:
            print('Wrong thing to get')

    def search(self):
        makes, models, end_of_counter = self.get_products_make_and_model('offer-title__link')
        mileages = self.get_products('mileage', end_of_counter)
        years = self.get_products('year', end_of_counter)
        fuels = self.get_products('fuel', end_of_counter)
        engine_sizes = self.get_products('engine_size', end_of_counter)
        urls = self.get_products('url', end_of_counter)
        prices = self.get_products('price', end_of_counter)

        return makes, models, mileages, years, fuels, engine_sizes, urls, prices


trying = CarsScrapper()
trying.search()
