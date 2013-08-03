# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Package'
        db.create_table(u'api_package', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500, db_index=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500)),
            ('created_at', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'api', ['Package'])

        # Adding unique constraint on 'Package', fields ['name', 'url']
        db.create_unique(u'api_package', ['name', 'url'])


    def backwards(self, orm):
        # Removing unique constraint on 'Package', fields ['name', 'url']
        db.delete_unique(u'api_package', ['name', 'url'])

        # Deleting model 'Package'
        db.delete_table(u'api_package')


    models = {
        u'api.package': {
            'Meta': {'unique_together': "(('name', 'url'),)", 'object_name': 'Package'},
            'created_at': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500', 'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'})
        }
    }

    complete_apps = ['api']