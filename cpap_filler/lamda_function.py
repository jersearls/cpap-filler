import logging
from pumper import Pumper
from dotenv import load_dotenv

#def lambda_handler(event, context):
#    load_dotenv(find_dotenv())
#    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
#    logger = logging.getLogger()
#    logger.setLevel(logging.DEBUG)
#    Pumper().run()

def run():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    Pumper().run()
run()
