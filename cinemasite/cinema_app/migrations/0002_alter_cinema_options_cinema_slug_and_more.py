# Generated by Django 5.0.6 on 2024-06-04 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cinema',
            options={'ordering': ['-time_create']},
        ),
        migrations.AddField(
            model_name='cinema',
            name='slug',
            field=models.SlugField(blank=True, max_length=255),
        ),
        migrations.AddIndex(
            model_name='cinema',
            index=models.Index(fields=['-time_create'], name='cinema_app__time_cr_32d7ab_idx'),
        ),
    ]
