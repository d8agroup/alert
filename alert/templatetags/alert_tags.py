import json

from django.template import Library

register = Library()


@register.filter('jsonify')
def jsonify(obj):
    return json.dumps(obj)


@register.filter('is_admin')
def is_admin(user):
    if not user.is_authenticated():
        return False
    if user.is_superuser or user.is_staff:
        return True
    return bool(user.groups.filter(name='Admins'))


@register.filter('is_curator')
def is_curator(user):
    if not user.is_authenticated():
        return False
    if user.is_superuser or user.is_staff:
        return True
    return bool(user.groups.filter(name='Curators'))