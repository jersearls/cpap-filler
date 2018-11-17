# cpap-filler

Python project to scrape CPAP usage data and call an arduino to fill a CPAP water reservoir.

This project utilizes a particle photon device that has been flashed with [this code repository](https://github.com/jersearls/cpap-filler-arduino) and requires a [peristaltic pump](https://www.amazon.com/gp/product/B00VHYO9F0/ref=oh_aui_detailpage_o07_s00?ie=UTF8&psc=1) controlled by pin D3. 

This project also assumes the CPAP machine used is the [Resmed Airsense 10](https://www.resmed.com/us/en/consumer/products/devices/airsense-10-cpap.html). 

## Installation

This project uses Pipenv to manage dependencies.

* To install dependencies, first install Pipenv with the `brew install pipenv` command

* With pipenv installed run `pipenv install` from the root of the project

* Fill variables as shown in `.env.example` file into an empty `.env` file at the project root
	* Particle device ID and auth token can be found [within the particle web IDE](https://build.particle.io/) under `devices` and `settings`.


## Working with CPAP Filler
### Local Execution

To run the program locally, execute the following bash script from the root of the project:

```bash
./bin/run
```

### Running on a Local CRON

```bash
env EDITOR=vim crontab -e
```

Cron command to run filler at 1:30pm every day

`30 13 * * * <path_to_repo>/cpap-filler/bin/run`

#### Note for Mojave Users

Crontab needs access to user libraries to execute dependencies. This access was revoked in MacOS Mojave. [Click here](https://blog.bejarano.io/fixing-cron-jobs-in-mojave.html) to learn how to implement a fix. 

### Deploy to AWS Lambda

To create a deployable zip file of the project that can be uploaded to AWS Lambda, execute the following bash script from the root of the project:

```bash
./bin/build_and_deploy
```

The `/tmp` folder created by the script contains the deployable zip file.

### Pump Calibration

Before using the machine you will need to calibrate the pump output.

A script is included to facilitate this.

Place the pump above a graduated cylinder.

From the root directory run the following command and answer the prompts:

```bash
pipenv run python calibrate/calibrate.py
```

The script will output a mL/s value. This value will be added to the local `.env` file automatically after running calibration.



#### CPAP Device Water Consumption

The Airsense 10 water reservoir holds 380mL at MAX line. 
Each quarter tick mark is placed at 95mL increments.

At a humidity level of 4, the machine uses roughly one quarter tank per 7 hours.

Testing has shown consumption at approximately 15 mL/hr.

This variable is subject to change with varying humidity and weather. 

It is stored as an environmental variable in the `.env` file. 

