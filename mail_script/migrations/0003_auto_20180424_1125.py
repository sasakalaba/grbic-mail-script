# Generated by Django 2.0.4 on 2018-04-24 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_script', '0002_auto_20180424_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='emails_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='directory',
            name='urls_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
