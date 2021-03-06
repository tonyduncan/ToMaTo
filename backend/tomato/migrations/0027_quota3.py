# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Quota'
        db.create_table('tomato_quota', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monthly', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['tomato.Usage'])),
            ('used', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['tomato.Usage'])),
            ('used_time', self.gf('django.db.models.fields.FloatField')()),
            ('continous_factor', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('tomato', ['Quota'])

        # Adding field 'User.quota'
        db.add_column('tomato_user', 'quota', self.gf('django.db.models.fields.related.OneToOneField')(related_name='+', unique=True, null=True, to=orm['tomato.Quota']), keep_default=False)

        # Changing field 'User.totalUsage'
        db.alter_column('tomato_user', 'totalUsage_id', self.gf('django.db.models.fields.related.OneToOneField')(default=-1, unique=True, to=orm['tomato.UsageStatistics']))

        # Deleting field 'UsageRecord.diskspace'
        db.delete_column('tomato_usagerecord', 'diskspace')

        # Deleting field 'UsageRecord.cputime'
        db.delete_column('tomato_usagerecord', 'cputime')

        # Deleting field 'UsageRecord.traffic'
        db.delete_column('tomato_usagerecord', 'traffic')

        # Deleting field 'UsageRecord.memory'
        db.delete_column('tomato_usagerecord', 'memory')

        # Changing field 'UsageRecord.usage'
        db.alter_column('tomato_usagerecord', 'usage_id', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['tomato.Usage']))


    def backwards(self, orm):
        
        # Deleting model 'Quota'
        db.delete_table('tomato_quota')

        # Deleting field 'User.quota'
        db.delete_column('tomato_user', 'quota_id')

        # Changing field 'User.totalUsage'
        db.alter_column('tomato_user', 'totalUsage_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['tomato.UsageStatistics']))

        # Adding field 'UsageRecord.diskspace'
        db.add_column('tomato_usagerecord', 'diskspace', self.gf('django.db.models.fields.FloatField')(default=0.0), keep_default=False)

        # Adding field 'UsageRecord.cputime'
        db.add_column('tomato_usagerecord', 'cputime', self.gf('django.db.models.fields.FloatField')(default=0.0), keep_default=False)

        # Adding field 'UsageRecord.traffic'
        db.add_column('tomato_usagerecord', 'traffic', self.gf('django.db.models.fields.FloatField')(default=0.0), keep_default=False)

        # Adding field 'UsageRecord.memory'
        db.add_column('tomato_usagerecord', 'memory', self.gf('django.db.models.fields.FloatField')(default=0.0), keep_default=False)

        # Changing field 'UsageRecord.usage'
        db.alter_column('tomato_usagerecord', 'usage_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['tomato.Usage']))


    models = {
        'tomato.connection': {
            'Meta': {'object_name': 'Connection'},
            'attrs': ('tomato.lib.db.JSONField', [], {}),
            'connection1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['tomato.HostConnection']"}),
            'connection2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['tomato.HostConnection']"}),
            'connectionElement1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['tomato.HostElement']"}),
            'connectionElement2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['tomato.HostElement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permissions': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Permissions']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'topology': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'connections'", 'to': "orm['tomato.Topology']"}),
            'totalUsage': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': "orm['tomato.UsageStatistics']"})
        },
        'tomato.element': {
            'Meta': {'object_name': 'Element'},
            'attrs': ('tomato.lib.db.JSONField', [], {}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'null': 'True', 'to': "orm['tomato.Connection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['tomato.Element']"}),
            'permissions': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Permissions']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'topology': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'to': "orm['tomato.Topology']"}),
            'totalUsage': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': "orm['tomato.UsageStatistics']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'tomato.external_network': {
            'Meta': {'object_name': 'External_Network', '_ormbases': ['tomato.Element']},
            'element_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Element']", 'unique': 'True', 'primary_key': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Network']", 'null': 'True'})
        },
        'tomato.external_network_endpoint': {
            'Meta': {'object_name': 'External_Network_Endpoint', '_ormbases': ['tomato.Element']},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.HostElement']", 'null': 'True'}),
            'element_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Element']", 'unique': 'True', 'primary_key': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.NetworkInstance']", 'null': 'True'})
        },
        'tomato.host': {
            'Meta': {'ordering': "['site', 'name']", 'object_name': 'Host'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'attrs': ('tomato.lib.db.JSONField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hosts'", 'to': "orm['tomato.Site']"}),
            'totalUsage': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': "orm['tomato.UsageStatistics']"})
        },
        'tomato.hostconnection': {
            'Meta': {'unique_together': "(('host', 'num'),)", 'object_name': 'HostConnection'},
            'attrs': ('tomato.lib.db.JSONField', [], {}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'connections'", 'to': "orm['tomato.Host']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'topology_connection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'host_connections'", 'null': 'True', 'to': "orm['tomato.Connection']"}),
            'topology_element': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'host_connections'", 'null': 'True', 'to': "orm['tomato.Element']"}),
            'usageStatistics': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': "orm['tomato.UsageStatistics']"})
        },
        'tomato.hostelement': {
            'Meta': {'unique_together': "(('host', 'num'),)", 'object_name': 'HostElement'},
            'attrs': ('tomato.lib.db.JSONField', [], {}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'to': "orm['tomato.Host']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'topology_connection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'host_elements'", 'null': 'True', 'to': "orm['tomato.Connection']"}),
            'topology_element': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'host_elements'", 'null': 'True', 'to': "orm['tomato.Element']"}),
            'usageStatistics': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': "orm['tomato.UsageStatistics']"})
        },
        'tomato.kvmqm': {
            'Meta': {'object_name': 'KVMQM'},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.HostElement']", 'null': 'True'}),
            'element_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Element']", 'unique': 'True', 'primary_key': 'True'}),
            'next_sync': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_index': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Profile']", 'null': 'True'}),
            'rextfv_last_started': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Site']", 'null': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Template']", 'null': 'True'})
        },
        'tomato.kvmqm_interface': {
            'Meta': {'object_name': 'KVMQM_Interface'},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.HostElement']", 'null': 'True'}),
            'element_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Element']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tomato.linkmeasurement': {
            'Meta': {'unique_together': "(('siteA', 'siteB', 'type', 'end'),)", 'object_name': 'LinkMeasurement'},
            'begin': ('django.db.models.fields.FloatField', [], {}),
            'delayAvg': ('django.db.models.fields.FloatField', [], {}),
            'delayStddev': ('django.db.models.fields.FloatField', [], {}),
            'end': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loss': ('django.db.models.fields.FloatField', [], {}),
            'measurements': ('django.db.models.fields.IntegerField', [], {}),
            'siteA': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['tomato.Site']"}),
            'siteB': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['tomato.Site']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'})
        },
        'tomato.network': {
            'Meta': {'object_name': 'Network', '_ormbases': ['tomato.Resource']},
            'kind': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'preference': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Resource']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tomato.networkinstance': {
            'Meta': {'unique_together': "(('host', 'bridge'),)", 'object_name': 'NetworkInstance', 'db_table': "'tomato_network_instance'", '_ormbases': ['tomato.Resource']},
            'bridge': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'networks'", 'to': "orm['tomato.Host']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['tomato.Network']"}),
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Resource']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tomato.openvz': {
            'Meta': {'object_name': 'OpenVZ'},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.HostElement']", 'null': 'True'}),
            'element_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Element']", 'unique': 'True', 'primary_key': 'True'}),
            'next_sync': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_index': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Profile']", 'null': 'True'}),
            'rextfv_last_started': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Site']", 'null': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Template']", 'null': 'True'})
        },
        'tomato.openvz_interface': {
            'Meta': {'object_name': 'OpenVZ_Interface'},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.HostElement']", 'null': 'True'}),
            'element_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Element']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tomato.organization': {
            'Meta': {'object_name': 'Organization'},
            'attrs': ('tomato.lib.db.JSONField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'totalUsage': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': "orm['tomato.UsageStatistics']"})
        },
        'tomato.permissionentry': {
            'Meta': {'unique_together': "(('user', 'set'),)", 'object_name': 'PermissionEntry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['tomato.Permissions']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.User']"})
        },
        'tomato.permissions': {
            'Meta': {'object_name': 'Permissions'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tomato.profile': {
            'Meta': {'object_name': 'Profile', '_ormbases': ['tomato.Resource']},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'preference': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Resource']", 'unique': 'True', 'primary_key': 'True'}),
            'tech': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'tomato.quota': {
            'Meta': {'object_name': 'Quota'},
            'continous_factor': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['tomato.Usage']"}),
            'used': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['tomato.Usage']"}),
            'used_time': ('django.db.models.fields.FloatField', [], {})
        },
        'tomato.repy': {
            'Meta': {'object_name': 'Repy'},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.HostElement']", 'null': 'True'}),
            'element_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Element']", 'unique': 'True', 'primary_key': 'True'}),
            'next_sync': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_index': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Profile']", 'null': 'True'}),
            'rextfv_last_started': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Site']", 'null': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Template']", 'null': 'True'})
        },
        'tomato.repy_interface': {
            'Meta': {'object_name': 'Repy_Interface'},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.HostElement']", 'null': 'True'}),
            'element_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Element']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tomato.resource': {
            'Meta': {'object_name': 'Resource'},
            'attrs': ('tomato.lib.db.JSONField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'tomato.site': {
            'Meta': {'object_name': 'Site'},
            'attrs': ('tomato.lib.db.JSONField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sites'", 'to': "orm['tomato.Organization']"})
        },
        'tomato.template': {
            'Meta': {'object_name': 'Template', '_ormbases': ['tomato.Resource']},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'preference': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Resource']", 'unique': 'True', 'primary_key': 'True'}),
            'tech': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'tomato.templateonhost': {
            'Meta': {'unique_together': "[('host', 'template')]", 'object_name': 'TemplateOnHost'},
            'date': ('django.db.models.fields.FloatField', [], {}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'templates'", 'to': "orm['tomato.Host']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hosts'", 'to': "orm['tomato.Template']"})
        },
        'tomato.tinc_endpoint': {
            'Meta': {'object_name': 'Tinc_Endpoint', '_ormbases': ['tomato.Element']},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.HostElement']", 'null': 'True'}),
            'element_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Element']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tomato.tinc_vpn': {
            'Meta': {'object_name': 'Tinc_VPN', '_ormbases': ['tomato.Element']},
            'element_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Element']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tomato.topology': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Topology'},
            'attrs': ('tomato.lib.db.JSONField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permissions': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.Permissions']"}),
            'timeout': ('django.db.models.fields.FloatField', [], {}),
            'timeout_step': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'totalUsage': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': "orm['tomato.UsageStatistics']"})
        },
        'tomato.udp_endpoint': {
            'Meta': {'object_name': 'UDP_Endpoint', '_ormbases': ['tomato.Element']},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tomato.HostElement']", 'null': 'True'}),
            'element_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tomato.Element']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tomato.usage': {
            'Meta': {'object_name': 'Usage'},
            'cputime': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'diskspace': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'traffic': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        'tomato.usagerecord': {
            'Meta': {'unique_together': "(('statistics', 'type', 'end'),)", 'object_name': 'UsageRecord'},
            'begin': ('django.db.models.fields.FloatField', [], {}),
            'end': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurements': ('django.db.models.fields.IntegerField', [], {}),
            'statistics': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'records'", 'to': "orm['tomato.UsageStatistics']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'usage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['tomato.Usage']"})
        },
        'tomato.usagestatistics': {
            'Meta': {'object_name': 'UsageStatistics'},
            'attrs': ('tomato.lib.db.JSONField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tomato.user': {
            'Meta': {'ordering': "['name', 'origin']", 'unique_together': "(('name', 'origin'),)", 'object_name': 'User'},
            'attrs': ('tomato.lib.db.JSONField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.FloatField', [], {'default': '1397465902.634502'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users'", 'to': "orm['tomato.Organization']"}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'password_time': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'quota': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': "orm['tomato.Quota']"}),
            'totalUsage': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['tomato.UsageStatistics']"})
        }
    }

    complete_apps = ['tomato']
