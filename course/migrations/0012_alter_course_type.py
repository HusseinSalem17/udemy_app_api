# Generated by Django 5.1.1 on 2024-11-26 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_alter_course_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='type',
            field=models.ManyToManyField(to='course.coursetype'),
        ),
    ]
