#!/usr/bin/env python3

''' 
River Warning System v 2.1 copyright 2017 Aaron Nelson (aaron.nelson805@gmail.com
This script retrieves weather data from waterdata.usgs.gov and sends an alert to facebook when 
stage trigger has been activated

copyright 2017 Aaron Nelson (aaron.nelson805@gmail.com)
'''

import requests
from bs4 import BeautifulSoup as BS
import facebook
import os
from datetime import datetime

#set some variables
now = datetime.now()
home = os.environ['HOME']
work = home + '/scripts/python/riverwarn/'
log = work + '/riverlog.txt'

with open(work + 'river_key', 'r') as keys:
    creds = eval(keys.read())

page_id = creds['fb_keys']['riverwarn']['page_id']
page_token = creds['fb_keys']['riverwarn']['token']
graph = facebook.GraphAPI(access_token = page_token)

def check_river(url):

    ALERT_LEVELS = ["major", "moderate", "flood", "action", "low"]
    river_link = 'https://water.weather.gov/ahps/'
    headers = {"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"}
    response = requests.get(url, headers=headers)
    soup = BS(response.text, 'lxml')

    data = []

    #process the data returned from waterdata.usgs.gov
    for river in soup.select("h1.data_name"):

        river_name = river.get_text(strip=True)
        river_data = river.find_next_sibling("div")
        data.append({
            "name": river_name,
            "stage": river_data.select_one(".stage_stage_flow").get_text(strip=True).replace("Latest Stage: ", ""),
            "flood_lvl": river_data.select_one(".flood_stage_flow").get_text(strip=True).replace("Flood Stage: ", "").replace(" Feet", ""),
            "warns": river_data.select_one(".current_warns_statmnts_ads > b").next_sibling.strip(),
            "alerts": {
            alert_name: alert_value.get_text(strip=True)
            for alert_name, alert_value in
         zip(ALERT_LEVELS, river_data.select(".flood_his_lwr .box_square table tr > td:nth-of-type(2)"))
        }
    })

    #define river data per station and set conditionals
    try:
        for n in range(len(data)):
            station = data[n]['name']

            if data[n]['stage'] == 'n/a' or data[n]['stage'] == 'Latest Flow: n/a' or data[n]['stage'] == 'Latest Stage: n/a':
                pass
            else:
                stage = float(data[n]['stage'])
                if data[n]['alerts'] == None:
                    pass
                else:
                    action = None
                    flood = None
                    moderate = None
                    major = None
                    for a in ALERT_LEVELS:
                        if a in data[n]['alerts'] and a != None:
                            action = float(data[n]['alerts']['action'])
                            flood = float(data[n]['alerts']['flood'])
                            moderate = float(data[n]['alerts']['moderate'])
                            major = float(data[n]['alerts']['major'])
                            warn = data[n]['warns']

                            if major == 0:
                                pass
                            elif moderate == 0:
                                pass
                            elif flood == 0:
                                pass
                            elif action == 0 and flood != 0:
                                action = flood
                        else:
                            pass

                    f = open(log, 'w')
                    f.write('[{}-{}-{}_{:d}:{:02d}] - Gauge check initiated..\n'.format(now.year, now.month, now.day, now.hour, now.minute))
                    if stage != None and action != None and stage < action :
                        pass
                    elif stage != None and major != None and major != 0 and stage > major :
                        graph.put_object(page_id, 'feed', message=('The {} has reached [Major Flood Stage: ({}Ft)].\n'
                                                                   '[Current Guage Depth]: {}Ft\n'
                                                                   '[Warnings]:{}\n'.format(station, major, stage, warn)), link=river_link)
                        f.write('[{}-{}-{}_{:d}:{:02d}]:{} - Stage check successful.\n'.format(now.year, now.month, now.day, now.hour, now.minute, url.title()))
                    elif stage != None and moderate != None and moderate != 0 and stage > moderate:
                        maj_diff = round((major - stage), 2)
                        graph.put_object(page_id, 'feed', message=('The {} has reached [Moderate Flood Stage]: {}Ft.\n'
                                                                   '[Current Guage Depth]: {}Ft.\n'
                                                                   '[Major Flood Stage] in {}ft.\n'
                                                                   '[Warnings]:[}\n'.format(station, moderate, stage, maj_diff, warn)), link= river_link)
                        f.write('[{}-{}-{}_{:d}:{:02d}]:{} - Stage check successful.\n'.format(now.year, now.month, now.day,now.hour, now.minute, url.title()))
                    elif stage != None and flood != None and flood != 0 and stage > flood:
                        mod_diff = round((moderate - stage), 2)
                        graph.put_object(page_id, 'feed', message=('The {} has reached [Flood Stage]: {}Ft.\n'
                                                                   '[Current Gauge Depth]: {}Ft.\n'
                                                                   '[Moderate Flood Stage] in {}Ft.\n'
                                                                   '[Warnings]: {}\n'.format(station, flood, stage, mod_diff, warn)), link= river_link)
                        f.write('[{}-{}-{}_{:d}:{:02d}]:{} - Stage check successful.\n'.format(now.year, now.month, now.day, now.hour, now.minute, url.title()))
                    elif stage != None and action != None and action != 0 and stage > action:
                        flood_diff = round((flood - stage), 2)
                        graph.put_object(page_id, 'feed', message=('The {} has reached [Action Stage]: {}Ft.\n'
                                                                   '[Current Gauge Depth]: {}Ft.\n'
                                                                   '[Flood Stage] in {}Ft.\n[Warnings]: {}\n'.format(station, action, stage, flood_diff, warn)), link= river_link)
                        f.write('[{}-{}-{}_{:d}:{:02d}]:{} - Stage check successful.\n'.format(now.year, now.month, now.day, now.hour, now.minute, url.title()))
                    f.close()
    except (facebook.GraphAPIError, requests.exceptions.ConnectionError):
        raise

def check_list(url_list):
    f = open(log, 'w')
    f.write('[{}-{}-{}_{:d}:{:02d}] - Gauge check initiated..\n'.format(now.year, now.month, now.day, now.hour, now.minute))
    for url in RIVER_URL:
         print(check_river(RIVER_URL[url]))
         f.write('[{}-{}-{}_{:d}:{:02d}]:{} - Stage check successful.\n'.format(now.year, now.month, now.day, now.hour, now.minute, url.title()))
    f.close()

def
if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='''River Flood Warning System v2.2''')
    parser.add_argument("-u", dest="url", type=check_river,
                        help="Check single river or stage. Enter URL")
    parser.add_argument("-l", dest="url_list", type=check_list,
                        help="enter river list file. 'eg river_list.txt'")

    args = parser.parse_args()
