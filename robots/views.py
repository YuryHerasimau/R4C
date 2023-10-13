from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from datetime import datetime

from .models import Robot
from .utils import validate_robot_creation, REQUIRED_TIMESTAMP


@csrf_exempt
def create_robot(request):
    """ API endpoint for creating a robot """
    if request.method == 'POST':
        try:
            data = validate_robot_creation(request)

            new_robot = Robot.objects.create(
                serial=f"{data['model']}-{data['version']}",
                model=data['model'],
                version=data['version'],
                created=datetime.strptime(data['created'], REQUIRED_TIMESTAMP)
            )
            return JsonResponse({'success': 'Robot created successfully'}, status=201)

        except Exception as ex:
            return JsonResponse({'error': f'{ex}'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
