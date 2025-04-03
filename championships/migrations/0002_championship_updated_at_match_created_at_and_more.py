# Generated by Django 5.2 on 2025-04-03 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championships', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='championship',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='match',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='team',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='team',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
