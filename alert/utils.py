from alert.themes.default.strings import SITE_STRINGS
from django_odc import api as odc
from django_odc.models import Dataset, Source
from django_odc.objects import ContentItem


def site_strings():
    #TODO This should be config driven
    return SITE_STRINGS


def get_curation_list(dataset_id, raw_search_data, request, exclude_content_ids=None, rows=20):
    search_data = {
        'sources': [{'guid': s['guid']} for s in raw_search_data['sources']],
        'filters': ['-id:%s' % content_id for content_id in exclude_content_ids],
        'facets': [],
        'pivots': [],
        'pagination': {'rows': rows}}
    search_results = odc.run_query_for_dataset(request.user, dataset_id, search_data)
    return search_results


def get_author_veracity(content_item):
    return 'none'


def record_curation_action(dataset_id, content_item, curation_direction, user):
    dataset = Dataset.GetById(dataset_id)
    content_item = ContentItem.FromDict(content_item)
    source = Source.GetById(content_item.source['id'])
    candidate_metadata = [m for m in content_item.metadata if m['key'] == 'metadata_alertstate_s']
    if candidate_metadata:
        candidate_metadata[0]['value'] = 'signal' if curation_direction == 'up' else 'noise'
    else:
        content_item.add_metadata('alertstate', 'signal' if curation_direction == 'up' else 'noise', 'string')
    dataset.send_data_to_datasetore(source, [content_item])
