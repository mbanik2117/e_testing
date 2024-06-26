# Generated by Django 5.0 on 2023-12-28 14:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_email'),
        ('setup', '0011_alter_useranswer_user_profile_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testattempt',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_attempts', to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='test_attempt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='setup.testattempt'),
        ),
    ]
