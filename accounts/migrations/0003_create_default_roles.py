from django.db import migrations


def create_roles(apps, schema_editor):
    Role = apps.get_model('accounts', 'Role')
    for name, desc in [
        ('guest', 'Guest'),
        ('user', 'Regular user'),
        ('moderator', 'Moderator'),
        ('administrator', 'Administrator'),
    ]:
        Role.objects.get_or_create(name=name, defaults={'description': desc})


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_role_auditlog_user_role'),
    ]

    operations = [
        migrations.RunPython(create_roles, noop),
    ]
