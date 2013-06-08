from alert.themes.default.strings import SITE_STRINGS
from django_odc import api as odc


def site_strings():
    #TODO This should be config driven
    return SITE_STRINGS


def get_curation_list(dataset_id, raw_search_data, request):
    search_data = {
        'sources': [{'guid': s['guid']} for s in raw_search_data['sources']],
        'filters': [],
        'facets': [],
        'pivots': [],
        'pagination': {'rows': 20}}
    search_results = odc.run_query_for_dataset(request.user, dataset_id, search_data)
    return search_results


