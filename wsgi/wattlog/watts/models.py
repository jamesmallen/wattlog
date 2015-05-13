from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone


# Create your models here.
class Measurement(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    watt_hours = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return "%s: %d whrs" % (self.timestamp, self.watt_hours)


class EstimatedMeasurement(object):
    timestamp = models.DateTimeField(auto_now_add=True)
    watt_hours = models.IntegerField(default=0, blank=True)


def get_estimated_measurement(timestamp):
    """
    Returns an estimated measurement object, using linear interpolation
    between the two nearest measurements recorded.
    """
    before = Measurement.objects.filter(timestamp__lte=timestamp).order_by('-timestamp').first()
    after = Measurement.objects.filter(timestamp__gte=timestamp).order_by('timestamp').first()

    if before is None:
        before = after
    elif after is None:
        after = before

    if after.watt_hours <= before.watt_hours:
        # watt_hours reset or is the same - just return the later value
        return after

    scale = (timestamp - before.timestamp).total_seconds() / (after.timestamp - before.timestamp).total_seconds()

    watt_hours = (1 - scale) * before.watt_hours + scale * after.watt_hours

    return Measurement(timestamp=timestamp, watt_hours=int(watt_hours))


def get_total_watt_hours(start_time, end_time=None):
    if end_time is None:
        end_time = timezone.now()
    start = get_estimated_measurement(start_time)
    end = get_estimated_measurement(end_time)

    return end.watt_hours - start.watt_hours

