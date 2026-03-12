# Generated for course project: pgvector extension and ListingEmbedding

import django.db.models.deletion
from django.db import migrations, models
from pgvector.django import VectorExtension, VectorField


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0002_location_apartments__town_id_cdeaf0_idx_and_more'),
        ('rent', '0001_initial'),
    ]

    operations = [
        VectorExtension(),
        migrations.CreateModel(
            name='ListingEmbedding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('embedding', VectorField(dimensions=1536)),
                ('model_name', models.CharField(blank=True, max_length=64)),
                ('apartment', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='embeddings',
                    to='apartments.apartment',
                )),
                ('rent', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='embeddings',
                    to='rent.rent',
                )),
            ],
            options={
                'db_table': 'apartments_listingembedding',
            },
        ),
        migrations.AddConstraint(
            model_name='listingembedding',
            constraint=models.CheckConstraint(
                check=(models.Q(('apartment__isnull', False), ('rent__isnull', True)) | models.Q(('apartment__isnull', True), ('rent__isnull', False))),
                name='listing_embedding_one_of_apartment_rent',
            ),
        ),
    ]
