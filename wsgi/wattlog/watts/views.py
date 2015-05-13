from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.utils.dateparse import parse_date, parse_datetime
from django.utils import timezone

from .models import Measurement, get_total_watt_hours
from .serializers import MeasurementSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


def datetime_or_date(s):
    return parse_datetime(s) or datetime.combine(parse_date(s), datetime.min.time())

@api_view(['GET'])
@permission_classes((AllowAny, ))
def total_watt_hours(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date is not None:
        start_time = datetime_or_date(start_date)
    else:
        # the beginning of time
        start_time = timezone.make_aware(datetime.min)

    if end_date is not None:
        end_time = datetime_or_date(end_date)
    else:
        end_time = timezone.now()

    # more exact overrides
    if 'start_time' in request.GET:
        start_time = parse_datetime(request.GET['start_time'])

    if 'end_time' in request.GET:
        start_time = parse_datetime(request.GET['end_time'])

    watt_hours = get_total_watt_hours(start_time, end_time)

    result = {
        'start_time': start_time,
        'end_time': end_time,
        'watt_hours': watt_hours,
    }

    return Response(result, status=status.HTTP_200_OK)
