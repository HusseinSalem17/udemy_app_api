# Generated by Django 5.1.1 on 2024-12-12 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_alter_course_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
