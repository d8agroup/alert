# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AuthorVeracity'
        db.create_table(u'alert_authorveracity', (
            ('author_id', self.gf('django.db.models.fields.TextField')(primary_key=True)),
            ('veracity', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'alert', ['AuthorVeracity'])


    def backwards(self, orm):
        # Deleting model 'AuthorVeracity'
        db.delete_table(u'alert_authorveracity')


    models = {
        u'alert.authorveracity': {
            'Meta': {'object_name': 'AuthorVeracity'},
            'author_id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'veracity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['alert']