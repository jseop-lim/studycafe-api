# Generated by Django 4.0.2 on 2022-02-27 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0004_alter_rent_real_end_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchase',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='rent',
            options={'ordering': ['-start_date']},
        ),
    ]
