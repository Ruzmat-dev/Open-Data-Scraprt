import logging

logger = logging.getLogger(__name__)
handler = logging.FileHandler('jobs/logs/scraper.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
