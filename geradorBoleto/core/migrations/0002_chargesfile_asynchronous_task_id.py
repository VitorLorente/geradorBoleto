# Generated by Django 5.1.1 on 2024-09-21 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chargesfile',
            name='asynchronous_task_id',
            field=models.CharField(default='04317400-8f34-4630-8d06-44716f04e8c7', max_length=36, verbose_name='Id da task assíncrona'),
            preserve_default=False,
        ),
    ]
