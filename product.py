import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
        self.sheet.update_cell(2, 1, 'Renault')

    def delete(self, row: int):
        self.sheet.delete_dimension('ROWS', row, row)

    def show(self):
        self.sheet.get_all_records()
