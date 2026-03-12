# Generated for course project: Lead model

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apartments', '0002_location_apartments__town_id_cdeaf0_idx_and_more'),
        ('rent', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_type', models.CharField(choices=[('sale', 'Sale'), ('rent', 'Rent')], max_length=10)),
                ('contact_info', models.TextField(blank=True)),
                ('message', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('contacted', 'Contacted'), ('closed', 'Closed')], default='new', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('apartment', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='leads',
                    to='apartments.apartment',
                )),
                ('rent', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='leads',
                    to='rent.rent',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='leads',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'db_table': 'leads_lead',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='lead',
            constraint=models.CheckConstraint(
                check=(models.Q(('apartment__isnull', False), ('rent__isnull', True)) | models.Q(('apartment__isnull', True), ('rent__isnull', False))),
                name='lead_one_of_apartment_rent',
            ),
        ),
    ]
