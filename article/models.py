from django.db import models

# Create your models here.
class actors(models.Model):
    id = models.IntegerField(primary_key=True)
    fir_name = models.CharField(max_length=100)
    sec_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1)

class directors(models.Model):
    id = models.IntegerField(primary_key=True)
    fir_name = models.CharField(max_length=100)
    sec_name = models.CharField(max_length=100)

class movies(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField(default=0)
    rank = models.FloatField()

class movie_director(models.Model):
    director_id = models.IntegerField(primary_key=True)
    movie_id = models.IntegerField(default=0)

class movie_genre(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=100)

class roles(models.Model):
    actor_id = models.IntegerField(primary_key=True)
    movie_id = models.IntegerField(default=0)
    role = models.CharField(max_length=100)
