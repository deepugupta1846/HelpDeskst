# Generated by Django 3.1.7 on 2021-03-22 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Help', '0015_auto_20210322_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='approved_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='approved_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='revoke_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='revoked_by',
            field=models.IntegerField(blank=True, max_length=3, null=True),
        ),
    ]
