# Generated by Django 4.2.8 on 2023-12-23 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0003_alter_testattempt_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='exams',
            field=models.ManyToManyField(to='setup.exam'),
        ),
    ]
