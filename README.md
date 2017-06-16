River Flood Warning System v2.1
copyright Aaron Nelson 2017 (aaron.nelson805@gmail.com)

RiverWarn is a python3 script that will retrieve river gauge data from https://water.weather.gov and posts and alert to your 
Facebook account (or page you manage) when flood stages have been reached.

**USAGE:**
 - Once the initial script *riverwarn.py* is executed the flood check function is passed to a scheduler which runs every 2 hours. This delay can be changed at the top of the file where the variables are defined under `check_delay`. Future releases will provide an option to run the script once, or scheduled.
 - You will have to obtain a Facebook OAUTH Token (https://developers.facebook.com/docs/pages/getting-started). Future releases will provide a method for automatic token generation. Once you have your FB Token (note: if posting to a page you will need to obtain the page ID also), enter the values in the provided *river_key.txt.* file.
 - Finally you will need to populate your *river_list.txt* file with the URLS for the rivers you want to check. To find your URL you will need to visit http://water.weather.gov/ahps2/glance.php? and first select your region, and then river. Put the URL in *river_list.txt* using the dictionary format: `'river name':'river url'` The rivers currently in the list are for example purposes and can be replaced with different values.
 - It is preferable to add `riverwarn.py` to `/usr/bin/` or `/usr/sbin/` and set up **cron** to run at boot. A cronjob can be set to perform this function by executing the command: `crontab -e` and then on the last line enter `@reboot /path/to/riverwarn.py`
