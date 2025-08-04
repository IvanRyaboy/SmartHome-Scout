from apartments.models import ApartmentImage
import requests


def create_apartment_with_images(owner, form, files):
    apartment = form.save(commit=False)
    apartment.owner = owner
    apartment.save()

    images = files.getlist('image')
    for img in images:
        ApartmentImage.objects.create(apartment=apartment, image=img)
    return apartment


def update_apartment_images(apartment, files):
    images = files.getlist('image')
    for img in images:
        ApartmentImage.objects.create(apartment=apartment, image=img)


def get_data_from_flask_api():
    response = requests.get('flask_api_url')

    if response:
        print(response.json())
