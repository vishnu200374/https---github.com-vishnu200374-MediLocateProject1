# Generated by Django 4.2.1 on 2023-09-27 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0003_reportupload'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportupload',
            old_name='doctoeremail',
            new_name='doctoremail',
        ),
    ]
