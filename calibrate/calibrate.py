import requests
import os

#placeholder only for now
#TODO: Build Calibration Script

#user input when ready to start test
#run pump for 30 seconds
#enter water level
#compute ml/s

class Calibrate():
    def __init__(self):
        self.access_token = os.getenv("PARTICLE_ACCESS_TOKEN")
        self.device_id = os.getenv("PARTICLE_DEVICE_ID")

    def calculate_pump_rate(self):
        pump_rate_per_second_in_mL = 1.4
        cpap_water_usage_per_hour_in_mL = 18.0
        pump_seconds_per_usage_hour = cpap_water_usage_per_hour_in_mL / pump_rate_per_second_in_mL
        usage_float = self.time_to_float(usage_in_hours)
        pump_run_time = usage_float * pump_seconds_per_usage_hour
        return round(pump_run_time)

    def call_photon_pump_function(self, seconds):
        particle_funtion= "Pump"
        argument = seconds
        address = 'https://api.particle.io/v1/devices/{0}/{1}'.format(self.device_id, particle_funtion)
        data = {'args': argument, 'access_token': self.access_token}
        post = requests.post(address, data=data)

    def run(self):
        pump_seconds = 30
        user_ready = gets.chomp
        mL_dispensed = gets.chomp

        if user_ready == "y":
            print("Pumping for: {0} seconds.".format(pump_seconds))
            #self.call_photon_pump_function(pump_seconds)
        elif not get_device_status():
            print("Calibration aborted")

Calibrate().run()
