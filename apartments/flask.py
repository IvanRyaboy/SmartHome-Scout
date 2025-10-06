from environs import Env
import requests
from .models import IDS
from .serializers import ApartmentCreateSerializer


env = Env()
env.read_env()


def get_azure_token():
    url = f"https://login.microsoftonline.com/{env("SOCIAL_AUTH_MICROSOFT_TENANT_ID")}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": env("SOCIAL_AUTH_MICROSOFT_CLIENT_ID"),
        "client_secret": env("SOCIAL_AUTH_MICROSOFT_SECRET"),
        "scope": env("FLASK_AIP_SCOPE")
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")


def fetch_flask_data(apartment_id):
    token = get_azure_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f'http://flask:5000/apartments/{apartment_id}',
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data: {response.status_code}"}


def create_apartment_from_data(apartment_data):
    serializer = ApartmentCreateSerializer(
        data=apartment_data,
    )

    if serializer.is_valid():
        apartment = serializer.save()
        return apartment
    else:
        raise ValueError(f"Invalid data: {serializer.errors}")


def start_fetching_data():
    apartments = IDS.objects.filter(status='IDS')
    for apartment in apartments:
        apartment_id = apartment.apartment_id
        flask_data = fetch_flask_data(apartment_id)
        create_apartment_from_data(flask_data)
    return None
