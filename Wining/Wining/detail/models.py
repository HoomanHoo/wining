# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from user.models import WinUser


class WinDetailView(models.Model):
    detail_view_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("user.WinUser", models.DO_NOTHING, blank=True, null=True)
    wine = models.ForeignKey("WinWine", models.DO_NOTHING)
    detail_view_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "win_detail_view"


class WinWine(models.Model):
    wine_id = models.AutoField(primary_key=True)
    wine_name = models.CharField(max_length=150)
    wine_name_eng = models.CharField(max_length=150)
    wine_sort = models.IntegerField()
    wine_capacity = models.IntegerField(blank=True, null=True)
    wine_alc = models.DecimalField(max_digits=3, decimal_places=1)
    wine_dangdo = models.IntegerField()
    wind_sando = models.IntegerField()
    wine_tannin = models.IntegerField()
    wine_food = models.IntegerField()
    wine_image = models.CharField(max_length=200)
    wine_region = models.ForeignKey("WinWineRegion", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "win_wine"


class WinWineRegion(models.Model):
    wine_region_id = models.IntegerField(primary_key=True)
    wine_region = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "win_wine_region"
