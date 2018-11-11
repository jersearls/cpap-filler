import requests
import fileinput
import time
import re
from os import fdopen, remove, getenv
from tempfile import mkstemp
from shutil import move

class Calibrate():
    def __init__(self):
        self.access_token = getenv("PARTICLE_ACCESS_TOKEN")
        self.device_id = getenv("PARTICLE_DEVICE_ID")

    def replace_env_var(self, pump_rate):
        fh, abs_path = mkstemp()
        with fdopen(fh,'w') as new_file:
            with open('.env') as old_file:
                for line in old_file:
                    new_file.write(re.sub(r'PUMP_RATE=(.*)', "PUMP_RATE={0}".format(pump_rate), line))
        remove('.env')
        move(abs_path, '.env')

    def calculate_pump_rate(self, mL_dispensed):
        rate = mL_dispensed / 30.0
        return round(rate, 3)

    def call_photon_pump_function(self, seconds):
        particle_funtion= "Pump"
        argument = seconds
        address = 'https://api.particle.io/v1/devices/{0}/{1}'.format(self.device_id, particle_funtion)
        data = {'args': argument, 'access_token': self.access_token}
        post = requests.post(address, data=data)

    def run(self):
        pump_seconds = 30
        user_ready = input("Ready to being calibration? y/N: ")

        if user_ready == "y":
            print("Pumping for: {0} seconds.".format(pump_seconds))
            #self.call_photon_pump_function(pump_seconds)
            time.sleep(3)
            mL_dispensed = float(input("Enter the number of mL dispensed: "))
            pump_rate = self.calculate_pump_rate(mL_dispensed)
            print("Current pump rate is {0} mL per second.".format(pump_rate))
            self.replace_env_var(pump_rate)
        elif not get_device_status() or user_ready != "y":
            print("Calibration aborted")

Calibrate().run()
