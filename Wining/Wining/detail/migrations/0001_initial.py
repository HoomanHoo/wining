# Generated by Django 4.2.2 on 2023-07-09 14:54

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WinDetailView",
            fields=[
                ("detail_view_id", models.AutoField(primary_key=True, serialize=False)),
                ("detail_view_time", models.DateTimeField()),
            ],
            options={
                "db_table": "win_detail_view",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="WinWine",
            fields=[
                ("wine_id", models.AutoField(primary_key=True, serialize=False)),
                ("wine_name", models.CharField(max_length=150)),
                ("wine_sort", models.IntegerField()),
                ("wine_capacity", models.IntegerField(blank=True, null=True)),
                ("wine_alc", models.DecimalField(decimal_places=1, max_digits=3)),
                ("wine_dangdo", models.IntegerField()),
                ("wind_sando", models.IntegerField()),
                ("wine_tannin", models.IntegerField()),
                ("wine_food", models.IntegerField()),
                ("wine_image", models.CharField(max_length=200)),
            ],
            options={
                "db_table": "win_wine",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="WinWineRegion",
            fields=[
                (
                    "wine_region_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("wine_region", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "win_wine_region",
                "managed": False,
            },
        ),
    ]
