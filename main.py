from bs4 import BeautifulSoup as bs
import requests
import json

base_url = 'https://awsregion.info'
output_file = './data.json'


def format_list(region_data):
    return {
        'id': int(region_data[0]),
        'region': region_data[1],
        'name': region_data[2],
        'year': region_data[3]
    }


link = requests.get(base_url)
link = link.content

data = bs(link, 'lxml')

new_table = []
table = data.select('table')[0]

table_rows = table.find_all('tr')
for tr in table_rows:
    td = tr.select('td')
    row = [str(tr.get_text()).strip() for tr in td]
    if len(row) != 0:
        new_table.append(row)

table_without_country_flags = []
for val in new_table[1:]:
    pop = val.pop(2)
    table_without_country_flags.append(format_list(val))

with open(output_file, mode='w') as file:
    json.dump(table_without_country_flags, file, ensure_ascii=False, indent=4)
