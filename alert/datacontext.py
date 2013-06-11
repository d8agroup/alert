from django_odc.datacontext import Solr4xDataContent


class AlertODCDataContext(Solr4xDataContent):
    def _run_delete_if_needed(self, source, connection):
        # If this is an update only query then there may be no overriding source
        if not source:
            return
        per_source_limit = 10000
        results = connection.query(
            'source_id:%s' % source.guid, fl=['id'], sort='created_dt asc',
            rows=1000, fq=['-metadata_alertstate_s:signal'])
        number_over_limit = results._numFound - per_source_limit
        if number_over_limit <= 0:
            return
        items_to_delete = []
        for i in results.results:
            if len(items_to_delete) >= number_over_limit:
                break
            items_to_delete.append(i['id'])
        if items_to_delete:
            connection.delete(queries=['id:%s' % id for id in items_to_delete], commit=True)

