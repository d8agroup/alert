from django.conf import settings
from utils import site_strings as get_site_strings


def site_strings(request):
    return {'s': get_site_strings()}


def deployment_timestamp(request):
    return {'deployment_timestamp': settings.DEPLOYMENT_TIMESTAMP}
