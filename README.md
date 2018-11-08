# cpap-filler

Python project to scrape CPAP usage data and call an arduino to fill a CPAP water reservoir.

##Installation

This project uses Pipenv to manage dependencies

* To install dependencies, first install Pipenv with the `brew install pipenv` command

* With pipenv installed run `pipenv install` from the root of the project

* Fill variables as shown in `.env.example` file into an empty `.env` file at the project root


## Local Execution

To run the program locally:

* Type `pipenv shell` to enter virtual python environment

* Run the following commands:

```bash
cd cpap_filler/
python -c 'import lambda_function; lambda_function.lambda_handler("event", "context")'
```

## Configure water use

### Calibration

Before using the machine you will need to calibrate the pump output.

A script is included to facilitate this.

Place the pump above a graduated cylinder and primed with water.

From the root directory run the following command and answer the prompts:

```bash
python calibrate/calibrate.py
```

The script will output a mL/s value. This value will be added to the local `.env` file.

#### NOTE

The Airsense 10 water reservoir holds 380mL at MAX line. 
Each quarter tick mark is placed at 95mL increments.

At a humidity level of 4, the machine uses roughly one quarter tank per 7 hours.

This equates to around 13.57 mL/hour of water consumption.

This variable is subject to change with varying humidity and weather. 
It is stored as an environmental variable in the `.env` file. 

