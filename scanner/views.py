from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .services.processor import process_network


@csrf_exempt
def receive_network(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            result = process_network(data)

            return JsonResponse({
                "status": "success",
                "classification": result["classification"],
                "trust_score": result["trust_score"]
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })

    return JsonResponse({"error": "Invalid request"})