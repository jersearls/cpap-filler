import logging
from pumper import Pumper
from dotenv import load_dotenv
import boto3
import botocore.config


def lambda_handler(event, context):
    load_dotenv()
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    #cfg = botocore.config.Config(retries={'max_attempts': 0})
    #client = boto3.client('lambda', config=cfg)
    Pumper().run()
