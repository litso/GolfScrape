import os
import logging
import uuid
from scraper import Scraper

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def hello(event, context):
    url = 'https://cityofla.ezlinksgolf.com/index.html#/search'

    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    
    screenshot_file = "{}-{}".format(''.join(filter(str.isalpha, url)), str(uuid.uuid4()))
    driver = Scraper()
    
    # logger.info('Generate fixed height screenshot')
    # driver.scrape(url, '/tmp/{}-fixed.png'.format(screenshot_file), height=1024)
    
    logger.info('Scrape EZ Links')
    results = driver.scrape(url, '/tmp/{}-full.png'.format(screenshot_file))
    
    # driver.close()

    response = {
        "statusCode": 200,
        "body": results
    }

    return response
