import os
import re
import json
from datetime import date, timedelta
import requests
from dotenv import load_dotenv
from lxml import html

load_dotenv()

access_token = os.getenv("PARTICLE_ACCESS_TOKEN")
device_id = os.getenv("PARTICLE_DEVICE_ID")

def scrape_cpap():
    login_url = "https://myair.resmed.com/Default.aspx?redirectCountry=2"

    session_requests = requests.session()
    session_result = session_requests.get(login_url)
    session_tree = html.fromstring(session_result.text)
    authenticity_token = list(set(session_tree.xpath("//input[@name='__EVENTVALIDATION']/@value")))[0]
    view_state = list(set(session_tree.xpath("//input[@name='__VIEWSTATE']/@value")))[0]
    view_state_generator = list(set(session_tree.xpath("//input[@name='__VIEWSTATEGENERATOR']/@value")))[0]

    headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://myair.resmed.com',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://myair.resmed.com/Default.aspx',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    }

    data = {
    'UmbianScriptManager1_TSM': ';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:59e0a739-153b-40bd-883f-4e212fc43305:ea597d4b:b25378d2;Umbian.ComplianceEngine.Web.UI.Pages:en-US:5f70433d-13a4-47d8-bbdd-3417747d64ae:41692311;;Umbian.ComplianceEngine.Web.UI.Pages:en-US:5f70433d-13a4-47d8-bbdd-3417747d64ae:e4cb8b8c;Telerik.Web.UI:en-US:cd668efa-682a-4e93-b784-26f0724f247c:16e4e7cd:f7645509:22a6274a;Umbian.ComplianceEngine.Web.UI.Pages:en-US:5f70433d-13a4-47d8-bbdd-3417747d64ae:50947e3a;;Telerik.Web.UI, Version=2014.3.1209.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:cd668efa-682a-4e93-b784-26f0724f247c:ed16cbdc',
    '__LASTFOCUS': '',
    '__EVENTTARGET': 'ButtonSignIn',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': view_state,
    '__VIEWSTATEGENERATOR': view_state_generator,
    '__VIEWSTATEENCRYPTED': '',
    '__EVENTVALIDATION': authenticity_token,
    'ctl00$ctl00$HiddenLoginToken': '',
    'ctl00$ctl00$hiddenPasswordURL': 'https://myair.resmed.com/PasswordPolicy.aspx',
    'ctl00$ctl00$hiddenSupportURL': 'https://myair.resmed.com/Support.aspx',
    'ctl00$ctl00$hiddenAboutURL': 'https://myair.resmed.com/About.aspx',
    'ctl00$ctl00$PageContent$MainPageContent$textBoxEmailAddress': os.getenv('CPAP_USER_NAME'),
    'ctl00$ctl00$PageContent$MainPageContent$textBoxPassword': os.getenv('CPAP_PASSWORD'),
    'ctl00$ctl00$PageContent$MainPageContent$idsSessionId': '',
    'ctl00$ctl00$PageContent$MainPageContent$identifier': ''
    }

    post_result = session_requests.post(
        login_url, 
        headers=headers,
        data = data
    )

    source_html = post_result.text
    return source_html

def parse_scores_from_html():
    raw_html = scrape_cpap()
    tree = html.fromstring(raw_html)
    script = tree.xpath('//script[contains(., "myScores")]/text()')[0]
    my_scores_string = re.findall(r"\[(.*)\]", script)[0]
    my_scores_list = '[{0}]'.format(my_scores_string)
    json_scores = json.loads(my_scores_list) 

    return json_scores

def find_most_recent_score():
    score_json = parse_scores_from_html()
    yesterday = date.today() - timedelta(1)
    date_yesterday = yesterday.strftime("%A, %B %-d")
    for score in score_json:
        if score["ChartDate"] == date_yesterday:
            return score["UsageDisplay"]

def time_to_float(time_str):
    hours, minutes = time_str.split(':')
    return (int(hours)*60 + int(minutes)) / 60.0

def calculate_pump_time():
    usage_in_hours = find_most_recent_score()
    pump_rate_per_second_in_mL = 1.4
    cpap_water_usage_per_hour_in_mL = 20.0
    pump_seconds_per_usage_hour = cpap_water_usage_per_hour_in_mL / pump_rate_per_second_in_mL
    usage_float = time_to_float(usage_in_hours)
    pump_run_time = usage_float * pump_seconds_per_usage_hour
    return round(pump_run_time)

def get_device_status():
    address = 'https://api.particle.io/v1/devices/{0}'.format(device_id)
    headers = {'Authorization':'Bearer {0}'.format(access_token)}
    get = requests.get(address, headers=headers)
    device_response = get.json()
    return device_response['connected']

def run_pump(seconds):
    particle_funtion= "Pump"
    argument = seconds
    address = 'https://api.particle.io/v1/devices/{0}/{1}'.format(device_id, particle_funtion)
    data = {'args': argument, 'access_token': access_token}
    post = requests.post(address, data=data)

def run():
    pump_seconds = calculate_pump_time()
    if get_device_status() and pump_seconds != 0:
        print("Pumping for: {0} seconds.".format(pump_seconds))
        run_pump(pump_seconds)
    elif not get_device_status():
        print("Device not responding")
    else:
        print("CPAP data not available")

run()
