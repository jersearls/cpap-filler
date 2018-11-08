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

Airsense 10 water reservoir holds 380mL at MAX line. Each quartile is 95mL.

At a humidity level of 4, the machine uses roughly 18mL per hour. 

The pump pumps approx. 1.4mL per second of water.


