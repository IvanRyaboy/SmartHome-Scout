from smarthousescout.app_celery import celery
from .flask import start_fetching_data
import logging


logger = logging.getLogger(__name__)


@celery.task(name='tasks.start_fetching_flask_data', bind=True)
def start_fetching_flask_data(self):
    """Дёргает ручку на flask api с данными новых квартир и записывает в бд"""
    try:
        logger.info("Начало получения данных с flask")
        result = start_fetching_data()
        logger.info("Получение данных успешно завершено")
        return {'status': 'success'}
    except Exception as e:
        logger.error(f"Ошибка получения данных {str(e)}")
        self.retry(exc=e, countdown=60, max_retries=3)
