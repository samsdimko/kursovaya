# Generated by Django 3.1.2 on 2020-11-02 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('descript', '0002_remove_answerchoice_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=200)),
            ],
        ),
    ]
