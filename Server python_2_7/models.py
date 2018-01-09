# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Artists(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'Artists'


class Lyrics(models.Model):
    lyrics = models.TextField(blank=True, null=True)
    seed = models.ForeignKey('Seed', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Lyrics'


class Seed(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    artist_hotttnesss = models.FloatField(blank=True, null=True)
    artist_id = models.CharField(max_length=255, blank=True, null=True)
    artist_name = models.CharField(max_length=255, blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    familiarity = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    release_id = models.CharField(max_length=255, blank=True, null=True)
    release_name = models.CharField(max_length=255, blank=True, null=True)
    similar = models.CharField(max_length=255, blank=True, null=True)
    song_hotttnesss = models.FloatField(blank=True, null=True)
    song_id = models.CharField(max_length=255, blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    terms = models.CharField(max_length=255, blank=True, null=True)
    year = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Seed'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
