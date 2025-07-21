from apartments.models import ApartmentImage


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
