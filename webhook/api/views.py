from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'GET':
        print("GET request received for WhatsApp webhook")
        print("Request GET parameters:", request.GET)

        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == 'demo':
            return HttpResponse(challenge, status=200)  # ✅ Texto plano
        return HttpResponse("Forbidden", status=403)

    if request.method == 'POST':
        data = json.loads(request.body)
        print("Mensaje recibido:", data)
        return JsonResponse({'status': 'received'}, status=200)
