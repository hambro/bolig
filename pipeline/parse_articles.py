import re

from bs4 import BeautifulSoup


def _clean(text):
    text = text.replace('\xa0', ' ').replace(',-', '').replace(' m²', '')
    try:
        text = int(re.sub(r'kr$', '', text).replace(' ', ''))
    except ValueError:
        pass

    return text


def _parse_data_lists(html):
    data = {}
    skip_keys = {'Mobil', 'Fax', ''}  # Unhandled data list labels

    for el in html.find('dl'):
        values_list = iter(el.find('dt, dd'))
        for a in values_list:
            _key = a.text
            a = next(values_list)
            if _key in skip_keys:
                continue
            data[_key] = _clean(a.text)

    return data


def parse_files():

    soup = BeautifulSoup(h, 'html.parser')


FACILITY_DATA_MAP = {
    "Postadresse": {"address": False}
}


def _parse_facility_data(html):
    facilities = html.find("div[data-controller=moreKeyInfo] li")
    facility_dict = [el.text for el in facilities]

    pass
