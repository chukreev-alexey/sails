# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Settings'
        db.create_table('website_settings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('common.fields.MultiEmailField')(max_length=255)),
        ))
        db.send_create_signal('website', ['Settings'])

        # Adding model 'Country'
        db.create_table('website_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('website', ['Country'])

        # Adding model 'Oper'
        db.create_table('website_oper', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('website', ['Oper'])

        # Adding model 'Currency'
        db.create_table('website_currency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('website', ['Currency'])

        # Adding model 'Office'
        db.create_table('website_office', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('website', ['Office'])

        # Adding model 'Staff'
        db.create_table('website_staff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('office', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Office'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('website', ['Staff'])

        # Adding model 'Order'
        db.create_table('website_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Staff'])),
            ('dt_mod', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('tourist', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Country'])),
            ('dt_in', self.gf('django.db.models.fields.DateField')()),
            ('oper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Oper'])),
            ('order_value', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=4)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Currency'])),
        ))
        db.send_create_signal('website', ['Order'])

        # Adding model 'Payment'
        db.create_table('website_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dt_mod', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payments', to=orm['website.Order'])),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Staff'])),
            ('pay', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=4)),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=4)),
            ('checked', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('website', ['Payment'])


    def backwards(self, orm):
        
        # Deleting model 'Settings'
        db.delete_table('website_settings')

        # Deleting model 'Country'
        db.delete_table('website_country')

        # Deleting model 'Oper'
        db.delete_table('website_oper')

        # Deleting model 'Currency'
        db.delete_table('website_currency')

        # Deleting model 'Office'
        db.delete_table('website_office')

        # Deleting model 'Staff'
        db.delete_table('website_staff')

        # Deleting model 'Order'
        db.delete_table('website_order')

        # Deleting model 'Payment'
        db.delete_table('website_payment')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'website.currency': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'website.office': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Office'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'website.oper': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Oper'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'website.order': {
            'Meta': {'ordering': "('-dt_mod',)", 'object_name': 'Order'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Country']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Currency']"}),
            'dt_in': ('django.db.models.fields.DateField', [], {}),
            'dt_mod': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Oper']"}),
            'order_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '4'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Staff']"}),
            'tourist': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'website.payment': {
            'Meta': {'ordering': "('-dt_mod',)", 'object_name': 'Payment'},
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dt_mod': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments'", 'to': "orm['website.Order']"}),
            'pay': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '4'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '4'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Staff']"})
        },
        'website.settings': {
            'Meta': {'object_name': 'Settings'},
            'email': ('common.fields.MultiEmailField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'website.staff': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Staff'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Office']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['website']
