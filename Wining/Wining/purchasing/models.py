from django.db import models
from user.models import WinUser
from store.models import WinSell

# Create your models here.


class WinPurchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("user.WinUser", models.DO_NOTHING)
    purchase_time = models.DateTimeField()
    purchase_number = models.IntegerField()
    purchase_price = models.IntegerField()

    class Meta:
        managed = False
        db_table = "win_purchase"


class WinPurchaseDetail(models.Model):
    purchase_detail_id = models.AutoField(primary_key=True)
    purchase = models.ForeignKey(WinPurchase, models.DO_NOTHING)
    sell = models.ForeignKey("store.WinSell", models.DO_NOTHING)
    purchase_det_number = models.IntegerField()
    purchase_det_price = models.IntegerField()
    purchase_det_state = models.IntegerField()

    class Meta:
      #  managed = False
        db_table = "win_purchase_detail"


class WinCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("user.WinUser", models.DO_NOTHING)
    cart_time = models.DateTimeField()
    cart_state = models.IntegerField()

    class Meta:
    #    managed = False
        db_table = "win_cart"


class WinCartDetail(models.Model):
    cart_det_id = models.AutoField(primary_key=True)
    sell = models.ForeignKey("store.WinSell", models.DO_NOTHING)
    cart = models.ForeignKey("WinCart", models.DO_NOTHING)
    cart_det_qnty = models.IntegerField()

    class Meta:
        managed = False
        db_table = "win_cart_detail"


class WinReceiveCode(models.Model):
    receive_code_id = models.AutoField(primary_key=True)
    receive_code = models.CharField(max_length=200)
    
    class Meta:
        db_table = "win_receive_code"