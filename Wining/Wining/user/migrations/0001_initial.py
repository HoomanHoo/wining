# Generated by Django 4.2.2 on 2023-07-09 14:54

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WinUser",
            fields=[
                (
                    "user_id",
                    models.CharField(max_length=30, primary_key=True, serialize=False),
                ),
                ("user_passwd", models.CharField(max_length=30)),
                ("user_name", models.CharField(max_length=20)),
                ("user_email", models.CharField(max_length=50)),
                ("user_tel", models.CharField(max_length=20)),
                ("user_reg_date", models.DateTimeField()),
                ("user_point", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "win_user",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="WinUserGrade",
            fields=[
                ("user_grade", models.IntegerField(primary_key=True, serialize=False)),
                ("user_grade_name", models.CharField(max_length=30, unique=True)),
            ],
            options={
                "db_table": "win_user_grade",
                "managed": False,
            },
        ),
    ]
