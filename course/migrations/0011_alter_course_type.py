# Generated by Django 5.1.1 on 2024-11-26 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_course_down_num_course_videos_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='type',
            field=models.ManyToManyField(blank=True, null=True, to='course.coursetype'),
        ),
    ]
