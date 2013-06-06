from utils import site_strings as get_site_strings


def site_strings(request):
    return {'s': get_site_strings()}