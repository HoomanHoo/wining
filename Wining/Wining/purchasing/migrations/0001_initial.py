# Generated by Django 4.2.2 on 2023-07-11 06:01

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WinCart",
            fields=[
                ("cart_id", models.IntegerField(primary_key=True, serialize=False)),
                ("cart_time", models.DateTimeField()),
                ("cart_state", models.IntegerField()),
            ],
            options={
                "db_table": "win_cart",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="WinCartDetail",
            fields=[
                ("cart_det_id", models.AutoField(primary_key=True, serialize=False)),
                ("cart_det_qnty", models.IntegerField()),
            ],
            options={
                "db_table": "win_cart_detail",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="WinPurchase",
            fields=[
                ("purchase_id", models.AutoField(primary_key=True, serialize=False)),
                ("purchase_time", models.DateTimeField()),
                ("purchase_number", models.IntegerField()),
                ("purchase_price", models.IntegerField()),
            ],
            options={
                "db_table": "win_purchase",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="WinPurchaseDetail",
            fields=[
                (
                    "purchase_detail_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("purchase_det_number", models.IntegerField()),
                ("purchase_det_price", models.IntegerField()),
                ("purchase_det_state", models.IntegerField()),
            ],
            options={
                "db_table": "win_purchase_detail",
                "managed": False,
            },
        ),
    ]