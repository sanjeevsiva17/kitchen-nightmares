# Generated by Django 3.0.5 on 2020-05-03 22:27

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20200503_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskstate',
            name='state',
            field=django_fsm.FSMField(choices=[('NEW', 'NEW'), ('ACC', 'ACCEPTED'), ('COM', 'COMPLETED'), ('DEC', 'DECLINED'), ('CAN', 'CANCELED')], default='NEW', max_length=50, protected=True),
        ),
    ]