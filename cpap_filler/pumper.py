import requests
import logging
import os
from scraper import Scraper

class Pumper():
    def __init__(self):
        self.access_token = os.getenv("PARTICLE_ACCESS_TOKEN")
        self.device_id = os.getenv("PARTICLE_DEVICE_ID")
        self.pump_rate = float(os.getenv("PUMP_RATE"))
        self.consumption_rate = float(os.getenv("CONSUMPTION_RATE"))
        self.scraper = Scraper()
        self.logger = logging.getLogger(__name__)

    def time_to_float(self, time_str):
        hours, minutes = time_str.split(':')
        return (int(hours)*60 + int(minutes)) / 60.0

    def calculate_pump_time(self):
        usage_in_hours = self.scraper.find_most_recent_score()
        self.logger.info("Slept for {0} hours.".format(usage_in_hours))
        pump_rate_per_second_in_mL = self.pump_rate
        cpap_water_usage_per_hour_in_mL = self.consumption_rate
        pump_seconds_per_usage_hour = cpap_water_usage_per_hour_in_mL / pump_rate_per_second_in_mL
        usage_float = self.time_to_float(usage_in_hours)
        pump_run_time = usage_float * pump_seconds_per_usage_hour
        return round(pump_run_time)

    def get_device_status(self):
        address = 'https://api.particle.io/v1/devices/{0}'.format(self.device_id)
        headers = {'Authorization':'Bearer {0}'.format(self.access_token)}
        get = requests.get(address, headers=headers)
        device_response = get.json()
        return device_response['connected']

    def call_photon_pump_function(self, seconds):
        particle_funtion= "Pump"
        argument = seconds
        address = 'https://api.particle.io/v1/devices/{0}/{1}'.format(self.device_id, particle_funtion)
        data = {'args': argument, 'access_token': self.access_token}
        post = requests.post(address, data=data)

    def run(self):
        pump_seconds = self.calculate_pump_time()
        if self.get_device_status() and pump_seconds != 0:
            self.logger.info("Pumping for: {0} seconds.".format(pump_seconds))
            self.call_photon_pump_function(pump_seconds)
        elif not self.get_device_status():
            self.logger.warn("Device not responding")
        else:
            self.logger.warn("CPAP not used previous night.")

