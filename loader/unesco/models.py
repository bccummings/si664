from django.db import models

# Create your models here.

class Category(models.Model):

    # Fields
    name = models.CharField(max_length=128)

    # Methods
    def __str__(self):
        return self.name

class Region(models.Model):

    # Fields
    name = models.CharField(max_length=128)

    # Methods
    def __str__(self):
        return self.name

class Iso(models.Model):

    # Fields
    name = models.CharField(max_length=2)

    # Relationships
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

class States(models.Model):

    # Fields
    name = models.CharField(max_length=128)

    # Relationships
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    iso = models.OneToOneField(Iso, on_delete=models.CASCADE)

    # Methods
    def __str__(self):
        return self.name


class Site(models.Model):

    # Fields
    name = models.CharField(max_length=128)

    description = models.TextField(blank=True)
    justification = models.TextField(blank=True)
    year = models.IntegerField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    area_hectares = models.FloatField(blank=True, null=True)

    # Relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE)

    # Methods
    def __str__(self):
        return self.name
