from selenium import webdriver
from exceptions import WrongThingToGetError
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException as NSEE, ElementNotInteractableException as ENIE


def change_to_int(string: str) -> int:
    string = string.replace(' ', '')
    while True:
        try:
            string = int(string)
            break
        except ValueError:
            string = string[:-1]
    return string


def is_negotiable(string: str) -> str:
    if string == 'Do negocjacji':
        string = 'True'
    else:
        string = 'False'
    return string


def get_price_and_currency(price_with_currency: str):
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

    return int(price_with_currency), name_of_currency


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
                   '%5B0%5D=&search%5Bcountry%5D=&view=list&page=209'

        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        self.isclosed = False
        self.list_of_tuples = []
        self.count = 1

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
        self.negotiable = []

    def get_products_make_and_model(self, title_class_name: str):
        titles = self.driver.find_elements_by_class_name(title_class_name)

        for title in titles:
            if self.excluded_makes[0] in title.text or self.excluded_makes[1] in title.text or self.excluded_makes[2] \
                    in title.text or self.excluded_makes[3] in title.text or self.excluded_makes[4] in title.text:

                self.models.append(' '.join((title.text.split()[2:])))
                temp_makes = title.text.split()[:2]
                make = ' '.join(temp_makes)
                self.makes.append(make)
                temp_makes.clear()

            else:
                self.models.append(' '.join((title.text.split()[1:])))
                self.makes.append(title.text.split()[0])

        return self.makes, self.models

    def get_products(self, thing_to_get, counter):
        try:
            if thing_to_get == 'mileage':
                for i in range(1, counter + 1):
                    try:
                        mileage = self.driver.find_element_by_xpath(
                            f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}'
                            f']/div[2]/ul/li[2]/span')
                        self.mileages.append(change_to_int(mileage.text))

                    except NSEE:
                        mileage = 0000
                        self.mileages.append(mileage)

                return self.mileages

            elif thing_to_get == 'year':
                for i in range(1, counter + 1):
                    try:
                        year = self.driver.find_element_by_xpath(
                            f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}'
                            f']/div[2]/ul/li[1]/span')
                        self.years.append(int(year.text))

                    except NSEE:
                        year = 0000
                        self.years.append(year)

                return self.years

            elif thing_to_get == 'fuel':
                for i in range(1, counter + 1):
                    try:
                        fuel = self.driver.find_element_by_xpath(
                            f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}'
                            f']/div[2]/ul/li[4]/span')
                        self.fuels.append(fuel.text)

                    except NSEE:
                        fuel = 'Failed to get'
                        self.fuels.append(fuel)

                return self.fuels

            elif thing_to_get == 'engine_size':
                for i in range(1, counter + 1):
                    try:
                        engine_size = self.driver.find_element_by_xpath(
                            f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}'
                            f']/div[2]/ul/li[3]/span')
                        self.engine_sizes.append(change_to_int(engine_size.text))

                    except NSEE:
                        engine_size = 0000
                        self.engine_sizes.append(engine_size)

                return self.engine_sizes

            elif thing_to_get == 'url':
                self.urls = [url.get_attribute('href') for url in
                             self.driver.find_elements_by_class_name('offer-title__link')]

                return self.urls

            else:
                raise WrongThingToGetError

        except WrongThingToGetError:
            print('Wrong thing to get')

    def get_products_price_and_currency(self, counter):
        for i in range(1, counter + 1):
            try:
                price = self.driver.find_element_by_xpath(
                    f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/div[1]/div[5]/article[{i}'
                    f']/div[2]/div[2]/div/div[1]/span')
                value, currency = get_price_and_currency(price.text)
                self.prices.append(value)
                self.currencies.append(currency)

            except NSEE:
                value = 0000
                currency = 'Failed'
                self.prices.append(value)
                self.currencies.append(currency)

            try:
                negotiable = self.driver.find_element_by_xpath(
                    f'/html/body/div[4]/div[2]/section/div[2]/div[1]/div/d'
                    f'iv[1]/div[5]/article[{i}]/div[2]/div[2]/div/span').text
                self.negotiable.append(is_negotiable(negotiable))

            except NSEE:
                negotiable = 'Failed to get'
                self.negotiable.append(negotiable)

        return self.prices, self.currencies, self.negotiable

    def search(self):
        while True:
            if self.isclosed:
                break

            else:
                number_of_articles = len(self.driver.find_elements_by_tag_name('article'))

                makes, models = self.get_products_make_and_model('offer-title__link')
                mileages = self.get_products('mileage', number_of_articles)
                years = self.get_products('year', number_of_articles)
                fuels = self.get_products('fuel', number_of_articles)
                engine_sizes = self.get_products('engine_size', number_of_articles)
                urls = self.get_products('url', number_of_articles)
                prices, currencies, negotiable = self.get_products_price_and_currency(number_of_articles)

                for i in range(number_of_articles):
                    temporary_list = (makes[i], models[i], mileages[i], years[i], fuels[i],
                                      engine_sizes[i], urls[i], prices[i], currencies[i], negotiable[i])
                    self.list_of_tuples.append(temporary_list)
                    del temporary_list
                print(self.list_of_tuples)
                makes.clear(), models.clear(), mileages.clear(), years.clear(), fuels.clear(), engine_sizes.clear()
                urls.clear(), prices.clear(), currencies.clear(), negotiable.clear()

                self.next_page()

        return self.list_of_tuples

    def next_page(self):
        try:
            interupting_element = self.driver.find_element_by_xpath('/html/body/div[4]/div[15]/div/div/a')
            interupting_element.click()

        except ENIE:
            pass

        li_index = len(self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/section/div[2]/div[2]/ul')
                       .find_elements_by_tag_name('li'))

        if li_index == 7 and self.count == 2:
            self.isclosed = True
            self.driver.close()

        elif self.count == 1:
            nexts = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"/html/body/div[4]/div[2]/section/div[2]/div[2]/ul/li[{li_index}]/a"))
            )
            nexts.click()
            self.count = 2

        else:
            nexts = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                (By.XPATH, f'/html/body/div[4]/div[2]/section/div[2]/div[2]/ul/li[{li_index}]/a'))
            )
            nexts.click()


if __name__ == '__main__':
    temp = CarsScrapper().search()
    print(temp)
