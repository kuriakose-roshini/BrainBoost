# Generated by Django 5.1.7 on 2025-03-25 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0002_remove_customadmin_is_super_admin_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customadmin',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customadmin_set', related_query_name='customadmin', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='customadmin',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customadmin_set', related_query_name='customadmin', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
