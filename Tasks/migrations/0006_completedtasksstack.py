# Generated by Django 5.0 on 2024-01-02 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tasks', '0005_alter_task_urgency'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedTasksStack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_ids', models.TextField(default='')),
            ],
        ),
    ]
