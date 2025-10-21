from environs import Env
import requests
from .models import IDS, Rent
from .serializers import RentCreateSerializer
from django.db import transaction, IntegrityError
from psycopg2 import errorcodes
from accounts.utils import get_service_user

env = Env()
env.read_env()


def get_azure_token():
    """Возвращает токен для доступа к api flask"""
    url = f"https://login.microsoftonline.com/{env("SOCIAL_AUTH_MICROSOFT_TENANT_ID")}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": env("SOCIAL_AUTH_MICROSOFT_CLIENT_ID"),
        "client_secret": env("SOCIAL_AUTH_MICROSOFT_SECRET"),
        "scope": env("FLASK_AIP_SCOPE")
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")


def fetch_flask_data(rent_id):
    """Возвращает данные о арендных квартирах, id которых отправляются вебхуком из микросервиса на flask"""
    token = get_azure_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f'http://flask:5000/rent/{rent_id}',
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data: {response.status_code}"}


def _is_unique_violation(e: IntegrityError) -> bool:
    cause = getattr(e, '__cause__', None)
    return getattr(cause, 'pgcode', None) == errorcodes.UNIQUE_VIOLATION


def create_rent_from_data(rent_data):
    service_user = get_service_user()
    serializer = RentCreateSerializer(data=rent_data, context={'owner': service_user})
    serializer.is_valid(raise_exception=True)

    try:
        with transaction.atomic():
            rnt = serializer.save()
        return rnt, True, 'created'

    except IntegrityError as e:
        if _is_unique_violation(e):
            ext_id = rent_data.get('_id')
            if ext_id:
                existing = Rent.objects.filter(id=ext_id).first()
                if existing:
                    return existing, False, 'exists'

            link = rent_data.get('link')
            if link:
                existing = Rent.objects.filter(link=link).first()
                if existing:
                    return existing, False, 'exists'
            return None, False, 'duplicate_without_lookup'

        raise


def start_fetching_data():
    rent_apartments = IDS.objects.filter(status='IDS')
    for rent in rent_apartments:
        rent_id = rent.rent_id
        flask_data = fetch_flask_data(rent_id)
        create_rent_from_data(flask_data)
        rent.status = 'PROCESSED'
        rent.save(update_fields=['status'])
    return None


# if __name__ == "__name__":
#     print(fetch_flask_data('3892327'))
