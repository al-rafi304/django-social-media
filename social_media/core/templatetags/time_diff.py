from django import template
from django.utils import timezone


register = template.Library()

def time_format(time):
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

def number_format(num):
    new_num = str(num)
    if num > 999:
        new_num = str(round((num / 1000), 1)) + 'K'
    if num > 999999:
        new_num = str(round((num / 1000000), 1)) + 'M'
    if num > 999999999:
        new_num = str(round((num / 1000000000), 1)) + 'B'
    
    return new_num
         

register.filter('custom_time_format', time_format)
register.filter('custom_number_format', number_format)