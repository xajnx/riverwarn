#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as BS

def nws_alert(url):
    try:
        nws_url = 'http://water.weather.gov/ahps2/'
        headers = {"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"}
        response = requests.get(url, headers=headers)
        soup = BS(response.text, "lxml")
        f_warn = soup.find('a', attrs={'title': 'Flood Warning'})
        f_url = f_warn.get('href')
        flood_get = nws_url + f_url
        f_response = requests.get(flood_get, headers=headers)
        f_soup = BS(f_response.text, "lxml")
        text = f_soup.get_text(strip=True)
        return text
    except AttributeError:
        pass




