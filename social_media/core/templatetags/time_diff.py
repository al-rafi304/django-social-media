from django import template
from django.utils import timezone


register = template.Library()

def get_time_diff(time):
        time_diff = None
        diff = timezone.now() - time

        if diff.days <= 0:
            # Within a second
            if diff.seconds < 60:
                time_diff = str(diff.seconds) + 's'
            # More than a minute
            elif diff.seconds < 3600:
                time_diff = str(int(diff.seconds // 60)) + 'm'
            # More than an hour 
            else:
                time_diff = str(int((diff.seconds / 60) // 60)) + 'h'
        # More than a day
        elif diff.days < 30: 
            time_diff = str(diff.days) + 'd'
        # More than a month
        elif diff.days < 365:
            time_diff = time.strftime("%d %b")
        # More than a year
        else:
            time_diff = time.strftime("%d %b, %Y")

        return f"{time_diff}"

register.filter('custom_time_format', get_time_diff)