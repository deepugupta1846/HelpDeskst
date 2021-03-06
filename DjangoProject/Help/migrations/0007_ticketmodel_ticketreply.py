# Generated by Django 3.1.7 on 2021-03-13 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Help', '0006_auto_20210313_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, null=True)),
                ('categrories', models.CharField(choices=[('Backend', 'Backend'), ('Fronted', 'Fronted'), ('Android', 'Android')], max_length=100)),
                ('ticket_type', models.CharField(choices=[('New Devlopment', 'New Devlopment'), ('Update', 'Update'), ('Bug', 'Bug')], max_length=100)),
                ('question', models.CharField(max_length=250)),
                ('description', models.TextField(null=True)),
                ('ticket_raise_date', models.DateTimeField(null=True)),
                ('ticket_close_date', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Help.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='TicketReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_msg', models.TextField()),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Help.ticketmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Help.usermodel')),
            ],
        ),
    ]
