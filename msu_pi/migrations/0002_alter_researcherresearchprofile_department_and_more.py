# Generated by Django 4.2.1 on 2023-05-14 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msu_pi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researcherresearchprofile',
            name='department',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='researcherresearchprofile',
            name='description',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='researcherresearchprofile',
            name='embedding',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='researcherresearchprofile',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
