from django.http import JsonResponse, HttpRequest, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.conf import settings

import json
import os
import openpyxl
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from .models import Robot
from .utils import validate_robot_creation, REQUIRED_TIMESTAMP


@csrf_exempt
def create_robot(request: HttpRequest) -> JsonResponse:
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


@require_GET
def download_robot_summary(request: HttpRequest) -> FileResponse:
    """ API endpoint for downloading xls file with robot summary information """
    try:
        current_datetime = datetime.now()
        start_of_week = current_datetime - timedelta(days=7)
        robots = Robot.objects.filter(created__gte=start_of_week)
        models = robots.values_list('model', flat=True).distinct()

        workbook = openpyxl.Workbook()

        for model in models:
            sheet = workbook.create_sheet(title=model)
            sheet.column_dimensions['A'].width = 10
            sheet.column_dimensions['B'].width = 10
            sheet.column_dimensions['C'].width = 20
            sheet.append(["Модель", "Версия", "Количество за неделю"])

            robots_by_model = Robot.objects.filter(created__gte=start_of_week, model=model)
            for version in robots_by_model.values_list('version', flat=True).distinct():
                robots_by_version = robots_by_model.filter(version=version)
                count = robots_by_version.count()
                sheet.append([model, version, count])

        workbook.remove(workbook['Sheet'])

        filename = f'robot_summary_{start_of_week.strftime("%Y%m%d_%H%M%S")}.xlsx'
        workbook_folder = Path(settings.BASE_DIR, "summary")
        workbook_folder.mkdir(parents=True, exist_ok=True)
        workbook_file = workbook_folder / filename
        workbook.save(workbook_file)

        return FileResponse(open(workbook_file, "rb"), status=200)

    except Exception as ex:
        return JsonResponse({'error': f'{ex}'}, status=500)