# Generated by Django 4.1.7 on 2023-03-30 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_source_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.source'),
        ),
    ]
