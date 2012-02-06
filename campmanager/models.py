from django.db import models
from django.contrib.auth.models import User

CACHE_KEY = 'taj_stats'

# Create your models here.
class Burner(models.Model):
    user = models.ForeignKey(User)
    realname = models.CharField(max_length=200)
    mobile = models.CharField(max_length=100)
    arrival_date = models.DateField()

    def __str__(self):
        return "%s" % self.realname

    class Admin:
        pass

class SubCamp(models.Model):
    name = models.CharField(max_length=80)
    desc = models.CharField(max_length=1024)

    def __str__(self):
        return "SubCamp: %s" % self.name

    class Admin:
        pass


class Group(models.Model):
    TENT_CAMPING = 't'
    RV_CAMPING = 'r'
    OFFSITE_CAMPING = 'o'
    CAMP_SITE_TYPE_CHOICES = (
        (TENT_CAMPING, "Tent camping"),
        (RV_CAMPING, "RV Camping"),
        (OFFSITE_CAMPING, "Off-site lodging")
    )
    subcamp = models.ForeignKey(SubCamp)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=80)
    desc = models.CharField(max_length=1024)
    numpeople = models.IntegerField()
    type = models.CharField(max_length=1, choices=CAMP_SITE_TYPE_CHOICES, default=TENT_CAMPING)

    def __str__(self):
        return "Group: %s %d people" % (self.name, self.numpeople)

    class Admin:
        pass

class Area(models.Model):
    group = models.ForeignKey(Group)
    name = models.CharField(max_length=80)
    desc = models.CharField(max_length=1024)
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return "Area: %s (%d x %d)" % (self.name, self.width, self.height)

    class Admin:
        pass
