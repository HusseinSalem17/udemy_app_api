# Generated by Django 5.1.1 on 2024-10-31 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_remove_course_video_course_type_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='user',
            new_name='teacher',
        ),
        migrations.AlterField(
            model_name='course',
            name='type_id',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]