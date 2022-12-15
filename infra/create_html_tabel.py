from json2html import *

script = ""
with open('infra/html_script.txt', 'r') as file:
    script = file.read().replace('\n', '')


def create_html_tbale(tabel):
    return json2html.convert(json=tabel, table_attributes="id=\"info-table\" border=\"1\"") + script

# print(json2html.convert(json = infoFromJson,table_attributes="id=\"info-table\" border=\"1\"")+data)
