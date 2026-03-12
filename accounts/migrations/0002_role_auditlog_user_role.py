# Generated for course project: Role, AuditLog, CustomUser.role

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'db_table': 'accounts_role',
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.UUIDField(blank=True, db_index=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('table_name', models.CharField(max_length=128)),
                ('record_id', models.CharField(blank=True, max_length=64)),
                ('action', models.CharField(choices=[('insert', 'Insert'), ('update', 'Update'), ('delete', 'Delete')], max_length=10)),
                ('old_values', models.JSONField(blank=True, null=True)),
                ('new_values', models.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'accounts_auditlog',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='users',
                to='accounts.role',
            ),
        ),
    ]
