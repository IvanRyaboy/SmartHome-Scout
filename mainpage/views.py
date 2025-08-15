from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apartments.utils import get_data_from_flask_api
from apartments.models import IDS
import json


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class PropertyPageView(TemplateView):
    template_name = "property.html"


@csrf_exempt
def receive_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            apartments = data.get('ids', [])
            for apartment in apartments:
                IDS.objects.create(apartment_id=apartment, status='IDS')
            print(f"Receive data from Flask: {data}")
            return JsonResponse({"message": "Webhook received successfully!"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

