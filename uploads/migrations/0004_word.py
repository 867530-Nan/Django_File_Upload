# Generated by Django 2.1.4 on 2019-01-08 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0003_urlupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField(unique=True)),
                ('count', models.IntegerField()),
                ('frequency', models.FloatField(null=True)),
            ],
        ),
    ]