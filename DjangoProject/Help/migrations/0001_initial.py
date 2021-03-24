# Generated by Django 3.1.7 on 2021-03-08 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('mid_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('user_type', models.CharField(choices=[('Business team', 'Business team'), ('Developer', 'Developer'), ('Admin', 'Admin')], max_length=100)),
                ('password', models.CharField(default=None, max_length=100)),
                ('approved_by', models.CharField(max_length=100)),
                ('approved_date', models.DateField()),
            ],
        ),
    ]