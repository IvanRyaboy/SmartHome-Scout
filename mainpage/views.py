from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apartments.models import IDS as apartment_IDS
from rent.models import IDS as rent_IDS
import json


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class PropertyPageView(TemplateView):
    template_name = "property.html"


@csrf_exempt
def receive_apartments_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            apartments = data.get('ids', [])
            for apartment in apartments:
                apartment_IDS.objects.create(apartment_id=apartment, status='IDS')
            print(f"Receive data from Flask: {data}")
            return JsonResponse({"message": "Webhook received successfully!"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def receive_rent_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rent_apartments = data.get('ids', [])
            for rent in rent_apartments:
                rent_IDS.objects.create(rent_id=rent, status='IDS')
            print(f"Receive data from Flask: {data}")
            return JsonResponse({'message': 'Webhook received successfully!'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'})
