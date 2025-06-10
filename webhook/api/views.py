# app_whatsapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# @csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if mode == 'subscribe' and token == 'demo':
            return JsonResponse({'hub.challenge': challenge})
        return JsonResponse({}, status=403)

    if request.method == 'POST':
        data = json.loads(request.body)
        # Aquí guardarás o procesarás los mensajes entrantes
        print("Mensaje recibido:", data)
        return JsonResponse({'status': 'received'}, status=200)
    
