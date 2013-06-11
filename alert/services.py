from alert.models import AuthorVeracity
from django_odc.services import _BaseService


class AlertV01Service(_BaseService):
    _configuration = {
        'type': 'alert_v01',
        'images': {
            '16': '/static/img/odc/alert_16.png',
            '24': '/static/img/odc/alert_24.png',
            '32': '/static/img/odc/alert_32.png',
            '48': '/static/img/odc/alert_48.png',
            '64': '/static/img/odc/alert_64.png',
            '128': '/static/img/odc/alert_128.png'
        },
        'display_name_short': 'Alert',
        'display_name_full': 'Services for the Alert App',
        'description_short': 'Applies the content additions required for the alert app.',
        'description_full': 'Applies the content additions required for the alert app.',
        'config': {
            'type': 'none'
        }
    }

    def channel_data_type_is_supported(self, channel_data_type):
        # This service only supports content types
        return channel_data_type in 'content_v01'

    def run(self, config, data):
        if data:
            author_veracities = AuthorVeracity.GetManyByAuthorDisplayName(
                data[0].source['channel']['type'],
                [d.author.display_name for d in data])
            for d in data:
                d.add_metadata('alertstate', 'new', 'string')
                d.add_metadata('alertcurationviews', 0, 'int')
                d.add_metadata(
                    'alertauthorveracity',
                    author_veracities[d.author.display_name].veracity_as_string,
                    'string')
        return data