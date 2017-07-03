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
from fb_auth import get_token
import pause
from nws_alert import nws_alert

# set some variables
now = datetime.now()
home = os.environ['HOME']
work = home + '/scripts/python/'
log = work + 'riverwarn/riverlog.txt'

with open(work + 'apikeys', 'r') as keys:
    creds = eval(keys.read())

page_id = creds['fb_keys']['riverwarn']['page_id']
app_token = creds['fb_keys']['riverwarn']['token']
app_id = creds['fb_keys']['riverwarn']['app_id']
app_secret = creds['fb_keys']['riverwarn']['app_secret']
auth = get_token(app_id, app_secret, app_token)
graph = facebook.GraphAPI(access_token=auth)

with open(work + 'riverwarn/riverlist.txt', 'r') as rivers:
    RIVER_URL = eval(rivers.read())

def check_river(url):

    ALERT_LEVELS = ["major", "moderate", "flood", "action", "low"]
    flood_link = 'http://water.weather.gov/ahps2/hydrograph.php?wfo=lch&gage='
    # flood_map = 'http://water.weather.gov/ahps2/inundation/index.php?gage='
    headers = {"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"}
    response = requests.get(url, headers=headers)
    soup = BS(response.text, 'lxml')

    print('Checking url...{}'.format(url))
    data = []

    # process the data returned from waterdata.usgs.gov
    for river in soup.select("h1.data_name"):
        river_name = river.get_text(strip=True)
        river_data = river.find_next_sibling("div")
        stx_id = river.attrs['id']
        data.append({
            "name": river_name,
            "id": stx_id,
            "stage": river_data.select_one(".stage_stage_flow").get_text(strip=True).replace("Latest Stage: ", ""),
            "flood_lvl": river_data.select_one(".flood_stage_flow").get_text(strip=True).replace("Flood Stage: ", "").replace(" Feet", ""),
            "warns": river_data.select_one(".current_warns_statmnts_ads > b").next_sibling.strip(),
            "alerts": {
            alert_name: alert_value.get_text(strip=True)
            for alert_name, alert_value in
         zip(ALERT_LEVELS, river_data.select(".flood_his_lwr .box_square table tr > td:nth-of-type(2)"))
        }
    })

    # define river data per station and set conditionals
    try:
        for n in range(len(data)):
            station = data[n]['name']
            sta_id = data[n]['id']
            nws_link = flood_link + sta_id
            nws_warn = nws_alert(nws_link)

            print("Processing data for {}".format(sta_id))
            if data[n]['stage'] == 'n/a' or data[n]['stage'] == 'Latest Flow: n/a' or data[n]['stage'] == 'Latest Stage: n/a':
                pass
            else:
                stage = float(data[n]['stage'])
                if data[n]['alerts'] is None:
                    pass
                else:
                    action = None
                    flood = None
                    moderate = None
                    major = None
                    for a in ALERT_LEVELS:
                        if a in data[n]['alerts'] and a is not None:
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

                    '''The print statements below are for testing purposes'''
                    if stage is not None and action is not None and stage < action :
                        pass
                    elif stage is not None and major is not None and major != 0 and stage > major :
                        river_link = flood_link + sta_id
                        print('Checking gauge: {}'.format(str(sta_id)))
                        # print('The {} has reached [Major Flood Stage: ({}Ft)].\n'
                        #      '[Current Gauge Depth]: {}Ft\n'
                        #      '[Warnings]:{}\n'
                        #      'NWS Statement:\n '
                        #      '{}'.format(station, major, stage, nws_warn, river_link))
                        graph.put_object(page_id, 'feed', message=('The {} has reached [Major Flood Stage: ({}Ft)].\n'
                                                                   '[Current Gauge Depth]: {}Ft\n'
                                                                   '[Warnings]:{}\n'
                                                                   '[NWS Statement]:\n'
                                                                   '{}'.format(station, major, stage, warn, nws_warn)), link=river_link)
                    elif stage is not None and moderate is not None and moderate != 0 and stage > moderate:
                        river_link = flood_link + sta_id
                        print('Checking gauge: {}'.format(str(sta_id)))
                        maj_diff = round((major - stage), 2)
                        # print('The {} has reached [Moderate Flood Stage ({}Ft.)]: \n'
                        #      '[Current Gauge Depth]: {}Ft.\n'
                        #      '[Major Flood Stage] in {}ft.\n '
                        #      '[Warnings]:[}\n'
                        #      'NWS Statement:\n '
                        #      '{}'.format(station, moderate, stage, maj_diff, nws_warn, river_link))
                        graph.put_object(page_id, 'feed', message=('The {} has reached [Moderate Flood Stage: ({}Ft.)]\n'
                                                                   '[Current Gauge Depth]: {}Ft.\n'
                                                                   '[Major Flood Stage] in {}ft.\n '
                                                                   '[Warnings]:[}\n'
                                                                   '[NWS Statement]:\n'
                                                                   '{}'.format(station, moderate, stage, maj_diff, warn, nws_warn)), link=river_link)
                    elif stage is not None and flood is not None and flood != 0 and stage > flood:
                        river_link = flood_link + sta_id
                        print('Checking gauge: {}'.format(str(sta_id)))
                        mod_diff = round((moderate - stage), 2)
                        # print('The {} has reached [Flood Stage ({}Ft.)]:\n'
                        #      '[Current Gauge Depth]: {}Ft.\n'
                        #      '[Moderate Flood Stage] in {}Ft.\n'
                        #      '[Warnings]: {}\n'
                        #      'NWS Statement:\n '
                        #      '{}'.format(station, flood, stage, mod_diff, nws_warn, river_link))
                        graph.put_object(page_id, 'feed', message=('The {} has reached [Flood Stage: ({}Ft.)]\n'
                                                                   '[Current Gauge Depth]: {}Ft.\n'
                                                                   '[Moderate Flood Stage] in {}Ft.\n'
                                                                   '[Warnings]: {}\n'
                                                                   '[NWS Statement]:\n'
                                                                   '{}'.format(station, flood, stage, mod_diff, warn, nws_warn)), link=river_link)
                    elif stage is not None and action is not None and action != 0 and stage > action:
                        river_link = flood_link + sta_id
                        print('Checking gauge: {}'.format(str(sta_id)))
                        flood_diff = round((flood - stage), 2)
                        # print('The {} has reached [Action Stage ({}Ft.)]:\n'
                        #      '[Current Gauge Depth]: {}Ft.\n'
                        #      '[Flood Stage] in {}Ft.\n'
                        #      '[Warnings]: {}\n'
                        #      'NWS Statement:\n '
                        #      '{}'.format(station, action, stage, flood_diff, nws_warn, river_link))
                        graph.put_object(page_id, 'feed', message=('The {} has reached [Action Stage: ({}Ft.)]\n'
                                                                   '[Current Gauge Depth]: {}Ft.\n'
                                                                   '[Flood Stage] in {}Ft.\n'
                                                                   '[Warnings]: {}\n'
                                                                   '[NWS Statement]:\n'
                                                                   '{}'.format(station, action, stage, flood_diff, warn, nws_warn)), link=river_link)

                    f.write('[{}-{}-{}_{:d}:{:02d}]:{} - Stage check successful.\n'.format(now.year, now.month, now.day, now.hour, now.minute, url.capitalize()))
                    f.close()
    except (facebook.GraphAPIError, requests.exceptions.ConnectionError, KeyboardInterrupt) as e:
        if e == KeyboardInterrupt:
            print("Process cancelled by user. Exiting..")
        else:
            f = open(log, 'w+')
            f.write("An error has occured:\n {}".format(str(e)))
            f.close()

if __name__ == '__main__':

    with open(log, 'w+') as f:
        f.write('[{}-{}-{}_{:d}:{:02d}] - Gauge check initiated..\n'.format(now.year, now.month, now.day, now.hour, now.minute))
        for url in RIVER_URL:
            check_river(RIVER_URL[url])
            pause.seconds(5)
            f.write('[{}-{}-{}_{:d}:{:02d}]:{} - Stage check successful.\n'.format(now.year, now.month, now.day, now.hour,
                                                                               now.minute, url.capitalize()))