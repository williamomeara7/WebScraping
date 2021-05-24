
import csv

import pandas as pd

from pprint import pprint

from uniswap_requests import make_request

import concurrent


class CsvReader:
    def __init__(self, input_file, output_file):
        self.rows = []
        self.input_file = input_file
        self.output_file = output_file
        self.output = []
        self.read_csv()
        self.make_requests()
        self.csv_writer()

    def read_csv(self):
        with open(self.input_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                self.rows.append(row)
            return

    def make_requests(self):
        for row in self.rows[1:]:
            id = row[1]
            url = "https://www.uniprot.org/uniprot/?query=geneid:{}".format(id)
            p_id = make_request(url)
            line = "{},{},{},{}".format(row[0], row[1], p_id, url)

            output_url = "https://www.uniprot.org/uniprot/{}".format(p_id)
            line = "{},{},{},{}".format(row[0], row[1], p_id, output_url)
            print(line)

            self.output.append([row[0], row[1], p_id, output_url])
            # yield id, p_id, "https://www.uniprot.org/uniprot/{}".format(p_id)
            
    def csv_writer(self):
        with open(self.output_file, 'w') as f:
            # using csv.writer method from CSV package
            fields = ['Product Name', 'Entrez Gene ID', 'PID', 'URL']

            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(self.output)


if __name__ == '__main__':
    mt_csv = CsvReader(input_file="UniProt-Scrape.csv", output_file="output.csv")
    mt_csv.make_requests()

    pprint(mt_csv.output)
    # pprint(mt_csv.rows)
    #
    # for item in mt_csv.iterator():
    #     print (item)