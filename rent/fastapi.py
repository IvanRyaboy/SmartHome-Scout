import requests
import logging


logger = logging.getLogger(__name__)


def send_ids(ids):
    try:
        response = requests.post(
            url=f'http://tg-rag-bot:8080/rent',
            data=ids
        )
    except Exception as e:
        logger.error(f'Error while sending rent ids {e}')
