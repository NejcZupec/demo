# Generated by Django 5.2 on 2025-04-15 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_alter_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('open', 'Backlog'), ('in_progress', 'In Progress'), ('in_review', 'In Review'), ('completed', 'Completed')], default='open', max_length=20),
        ),
    ]
