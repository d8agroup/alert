import math
from random import shuffle
from threading import Thread
from alert.models import AuthorVeracity
from alert.themes.default.strings import SITE_STRINGS
from django_odc import api as odc
from django_odc.models import Dataset, Source
from django_odc.objects import ContentItem


def async(gen):
    def func(*args, **kwargs):
        it = gen(*args, **kwargs)
        result = it.next()
        Thread(target=lambda: list(it)).start()
        return result
    return func


def site_strings():
    #TODO This should be config driven
    return SITE_STRINGS


def get_curation_list(dataset_id, raw_search_data, request, exclude_content_ids=None, rows=20):
    if rows < 3:
        return {}

    # First only get new content that has high author veracity
    filters = ['metadata_alertstate_s:new', 'metadata_alertauthorveracity_s:high']
    filters += ['-id:%s' % content_id for content_id in exclude_content_ids]
    search_data = {
        'sources': [{'guid': s['guid']} for s in raw_search_data['sources']],
        'filters': filters,
        'facets': [],
        'pivots': [],
        'pagination': {'rows': rows}}
    high_veracity_results = odc.run_query_for_dataset(request.user, dataset_id, search_data)

    # Get new content that does not have high veracity
    filters = ['metadata_alertstate_s:new', '-metadata_alertauthorveracity_s:high']
    filters += ['-id:%s' % content_id for content_id in exclude_content_ids]
    search_data = {
        'sources': [{'guid': s['guid']} for s in raw_search_data['sources']],
        'filters': filters,
        'facets': [],
        'pivots': [],
        'pagination': {'rows': rows}}
    new_content_results = odc.run_query_for_dataset(request.user, dataset_id, search_data)

    # Then combine and compile the results TODO: This needs to be configured by an admin
    search_results = {'items': []}
    for x in xrange(int(math.ceil(float(rows) / 2))):
        if x < len(high_veracity_results['items']):
            high_veracity_result = high_veracity_results['items'][x]
            author_count = len(
                [i for i in search_results['items']
                 if i.author.display_name == high_veracity_result.author.display_name])
            if author_count < 2:
                search_results['items'].append(high_veracity_result)
    for item in new_content_results['items']:
        if len(search_results['items']) < rows:
            search_results['items'].append(item)
    shuffle(search_results['items'])
    return search_results


@async
def record_curation_action(dataset_id, content_item, curation_direction, user):
    yield
    dataset = Dataset.GetById(dataset_id)
    content_item = ContentItem.FromDict(content_item)
    source = Source.GetById(content_item.source['id'])
    candidate_metadata = [m for m in content_item.metadata if m['key'] == 'metadata_alertstate_s']
    if candidate_metadata:
        candidate_metadata[0]['value'] = 'signal' if curation_direction == 'up' else 'noise'
    else:
        content_item.add_metadata('alertstate', 'signal' if curation_direction == 'up' else 'noise', 'string')
    dataset.send_data_to_datasetore(source, [content_item])
    author_display_name = content_item.author.display_name
    if curation_direction == 'ignore':  # Do not adjust author veracity for ignore curation actions
        return
    if author_display_name:
        author_veracity = AuthorVeracity.GetByAuthorDisplayName(
            content_item.source['channel']['type'], author_display_name)
        if curation_direction == 'up':
            author_veracity.increment_veracity()
        elif curation_direction == 'down':
            author_veracity.decrement_veracity()
        for dataset in Dataset.GetAllForInstance():
            results = dataset.run_query({
                'filters': ['author_display_name:%s' % author_display_name],
                'pagination': {'rows': 100}})
            if results['items']:
                for item in results['items']:
                    candidate_metadata = [m for m in item.metadata if m['key'] == 'metadata_alertauthorveracity_s']
                    if candidate_metadata:
                        candidate_metadata[0]['value'] = author_veracity.veracity_as_string()
                    else:
                        item.add_metadata('alertauthorveracity', author_veracity.veracity_as_string(), 'string')
            dataset.send_data_to_datasetore(None, results['items'])
