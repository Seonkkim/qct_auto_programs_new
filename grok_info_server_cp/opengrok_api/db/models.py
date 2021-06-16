# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Build(models.Model):
    sp_id_fk = models.ForeignKey('Sp', db_column='sp_id_fk', on_delete=models.CASCADE)
    name = models.TextField()
    wiki = models.TextField(blank=True, null=True)
    release_note = models.TextField(blank=True, null=True)
    fastboot = models.TextField()
    qfil = models.TextField()
    status = models.IntegerField()
    release_date = models.TextField(db_column='RELEASE_DATE', blank=True, null=True)  # Field name made lowercase.
    apps_id = models.TextField(db_column='APPS_ID', blank=True, null=True)  # Field name made lowercase.
    au_tag = models.TextField(db_column='AU_TAG', blank=True, null=True)  # Field name made lowercase.
    gvm_id = models.TextField(db_column='GVM_ID', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'build'


class Sp(models.Model):
    name = models.TextField()
    version = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    wiki = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    project_name = models.TextField(db_column='PROJECT_NAME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sp'
'''
from django.db import models

class SP(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    version = models.TextField()
    category = models.TextField()
    wiki = models.TextField(null=True)
    description = models.TextField()
    project_name = models.TextField()
class Build(models.Model):
    id = models.AutoField(primary_key=True)
    sp_id_fk = models.ForeignKey(SP, on_delete=models.CASCADE)
    name = models.TextField()
    wiki = models.TextField(null=True)
    release_note = models.TextField(null=True)
    fastboot = models.TextField()
    qfil = models.TextField()
    status = models.TextField()
    description = models.TextField(null=True)
    release_date = models.TextField(null=True)
    apps_id = models.TextField(null=True)
    au_tag = models.TextField(null=True)
'''

