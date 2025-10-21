from smarthousescout.app_celery import celery
from .flask import start_fetching_data
from django.db import IntegrityError
from psycopg2 import errorcodes
import logging

logger = logging.getLogger(__name__)


@celery.task(name='tasks.start_fetching_rent_flask_data', bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def start_fetching_flask_data(self):
    try:
        logger.info("Начало получения данных с Flask API")
        result = start_fetching_data()
        logger.info("Получение данных успешно завершено")
        return {'status': 'success', 'result': result}

    except IntegrityError as e:
        cause = getattr(e, '__cause__', None)
        pgcode = getattr(cause, 'pgcode', None)

        if pgcode == errorcodes.UNIQUE_VIOLATION:
            logger.warning(f"Дубликат данных: {str(e)} — задача завершена без повторного запуска.")
            return {'status': 'exists', 'error': str(e)}

        logger.error(f"Ошибка базы данных: {str(e)} — пробуем повторить через 60 сек.")
        raise self.retry(exc=e, countdown=60, max_retries=3)

    except Exception as e:
        logger.error(f"Ошибка получения данных: {str(e)} — повтор через 60 сек.")
        raise self.retry(exc=e, countdown=60, max_retries=3)
